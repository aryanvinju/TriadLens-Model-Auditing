param([string]$Image = 'aryanvinju/se_miniproj:bf87c5b096b54de26ce6fcf651bc28eeb253d3a7')
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
Set-Location $root
$out = Join-Path $root 'output/verification'
New-Item -ItemType Directory -Force $out | Out-Null
function Check-Native { if ($LASTEXITCODE -ne 0) { throw "Native command failed: $LASTEXITCODE" } }
docker image inspect $Image --format '{{json .RepoDigests}}' | Set-Content "$out/image-digest.json"
Check-Native
docker run --rm --entrypoint sh $Image -c 'test ! -f /app/data/lungcancer.csv && test ! -f /app/models/qml.joblib && test ! -f /app/reports/metrics.json'
Check-Native
$container = docker run -d --name triadlens-verification-20261113 -p 127.0.0.1:5003:5000 --mount "type=bind,source=$root/models,target=/app/models,readonly" --mount "type=bind,source=$root/reports,target=/app/reports,readonly" $Image
Check-Native
function Wait-Ready([string]$Url) {
  for ($attempt=0; $attempt -lt 60; $attempt++) {
    try { $r=Invoke-RestMethod "$Url/health/ready"; if ($r.status -eq 'ready') { return $r } } catch {}
    Start-Sleep -Seconds 2
  }
  throw "Readiness timeout: $Url"
}
$dockerReady = Wait-Ready 'http://127.0.0.1:5003'
$request = Get-Content reports/example_request.json -Raw
$dockerPrediction = Invoke-RestMethod http://127.0.0.1:5003/api/predict -Method Post -ContentType application/json -Body $request
kubectl apply -f k8s/lung-lab.yaml
Check-Native
kubectl -n lung-lab create secret generic triadlens-models --from-file=models/scaler.joblib --from-file=models/ml.joblib --from-file=models/dl.pt --from-file=models/qml.joblib --dry-run=client -o yaml | kubectl apply -f - | Out-Null
Check-Native
kubectl -n lung-lab create secret generic triadlens-reports --from-file=reports/metrics.json --from-file=reports/test_predictions.csv --from-file=reports/example_request.json --from-file=reports/splits.json --dry-run=client -o yaml | kubectl apply -f - | Out-Null
Check-Native
kubectl -n lung-lab set image deployment/lung-lab "web=$Image"
Check-Native
kubectl -n lung-lab rollout restart deployment/lung-lab
Check-Native
kubectl -n lung-lab rollout status deployment/lung-lab --timeout=240s
Check-Native
kubectl -n lung-lab get pods -o json | Set-Content "$out/pods-two.json"
$forward = Start-Process kubectl -ArgumentList '-n','lung-lab','port-forward','service/lung-lab','5005:80','--address','127.0.0.1' -WindowStyle Hidden -PassThru -RedirectStandardOutput "$out/port-forward.txt" -RedirectStandardError "$out/port-forward-error.txt"
$kubeReady = Wait-Ready 'http://127.0.0.1:5005'
$kubePrediction = Invoke-RestMethod http://127.0.0.1:5005/api/predict -Method Post -ContentType application/json -Body $request
kubectl -n lung-lab scale deployment/lung-lab --replicas=3
Check-Native
kubectl -n lung-lab rollout status deployment/lung-lab --timeout=180s
Check-Native
kubectl -n lung-lab get pods -o json | Set-Content "$out/pods-three.json"
kubectl -n lung-lab scale deployment/lung-lab --replicas=2
Check-Native
kubectl -n lung-lab rollout status deployment/lung-lab --timeout=180s
Check-Native
$summary = [ordered]@{ verified_at_utc=[DateTime]::UtcNow.ToString('o'); image=$Image; container=$container; docker_ready=$dockerReady.status; docker_models=@($dockerPrediction.results.model); kubernetes_ready=$kubeReady.status; kubernetes_models=@($kubePrediction.results.model); scale_sequence=@(2,3,2); port_forward_pid=$forward.Id }
$summary | ConvertTo-Json -Depth 8 | Set-Content "$out/deployment.json"
$summary | ConvertTo-Json -Depth 8
