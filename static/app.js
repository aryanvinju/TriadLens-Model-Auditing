const form = document.querySelector('#prediction-form');
const errorBox = document.querySelector('#error');
const names = {ML:'ML · Logistic regression', DL:'DL · Neural network', QML:'QML · Quantum kernel SVM'};
const seenRows = new Set();
const loggedRows = new Set();
let loadedReference = null;
let loadedFeatures = null;
let lastFeatures = null;

async function readJSON(url, options) {
  const response = await fetch(url, options);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || data.status || 'Request failed.');
  return data;
}
function paragraph(className, value) { const p=document.createElement('p'); p.className=className; p.textContent=value; return p; }
function showError(message) { errorBox.textContent=message; errorBox.hidden=false; }
function cell(value) { const td=document.createElement('td'); td.textContent=String(value); return td; }
function currentInput() {
  const fields=Object.fromEntries(new FormData(form));
  const model=fields.model; delete fields.model;
  for(const key of Object.keys(fields)) if(key!=='GENDER') fields[key]=Number(fields[key]);
  return {model,features:fields};
}
function referenceFor(features) {
  return loadedReference && Object.keys(features).every(key=>features[key]===loadedFeatures[key]) ? loadedReference : null;
}
function addSessionRow(reference, data) {
  if (!reference || data.results.length!==3 || loggedRows.has(reference.row_id)) return;
  loggedRows.add(reference.row_id);
  document.querySelector('#session-empty')?.remove();
  const labels=Object.fromEntries(data.results.map(result=>[result.model,result.label]));
  const wrong=data.results.filter(result=>result.label!==reference.actual_label).length;
  const review=wrong?`${wrong} model(s) differ from saved label${data.comparison?.review_flag?'; disagreement':''}`:(data.comparison?.review_flag?'Model disagreement or age warning':'No review flag');
  const row=document.createElement('tr');
  for(const value of [reference.row_id,reference.actual_label,labels.ML,labels.DL,labels.QML,review]) row.append(cell(value));
  document.querySelector('#session-body').prepend(row);
}
function displayResults(data, reference) {
  document.querySelector('#flow-processing').textContent=`Validated 15 fields; ran ${data.results.map(result=>result.model).join(', ')} using saved preprocessing and model artifacts.`;
  document.querySelector('#flow-output').textContent=`${data.results.map(result=>`${result.model}: ${result.label}`).join('; ')}.${reference?` Saved dataset label: ${reference.actual_label}.`:''}`;
  const container=document.querySelector('#results'); container.replaceChildren();
  for(const result of data.results) {
    const card=document.createElement('div'); card.className='result';
    const head=document.createElement('div'); head.className='result-head';
    head.append(paragraph('result-title',names[result.model]),paragraph('result-label',result.label));
    card.append(head,paragraph('result-detail',`${result.score_type}: ${result.score.toFixed(3)}`));
    container.append(card);
  }
  const audit=document.querySelector('#audit'); audit.replaceChildren(); audit.hidden=!data.comparison;
  if(data.comparison) {
    const c=data.comparison;
    audit.append(paragraph('audit-title',c.unanimous?'All three labels agree':'Model labels disagree'));
    audit.append(paragraph('result-detail',`${c.agreement_count} of 3 models chose ${c.majority_dataset_label}. This is a descriptive dataset label, not a clinical decision.`));
    if(c.review_flag) audit.append(paragraph('warning',`Review: ${c.review_reasons.join('; ')}.`));
  }
  const referenceCheck=document.querySelector('#reference-check');
  referenceCheck.hidden=!reference;
  if(reference) {
    const checks=data.results.map(result=>`${result.model} ${result.label===reference.actual_label?'matches':'differs from'} dataset label`);
    const wrong=data.results.filter(result=>result.label!==reference.actual_label).length;
    referenceCheck.textContent=`Saved label: ${reference.actual_label}. ${checks.join('; ')}. ${wrong?`Review: ${wrong} model(s) differ from the saved label.`:'All selected models match the saved label.'}`;
    addSessionRow(reference,data);
  }
  const warning=document.querySelector('#warning'); warning.textContent=data.warnings.join(' '); warning.hidden=!data.warnings.length;
  const panel=document.querySelector('#sensitivity-panel'); panel.hidden=data.results.length!==3;
  document.querySelector('#sensitivity-summary').textContent='';
  document.querySelector('#sensitivity-body').replaceChildren();
}
async function runAudit() {
  errorBox.hidden=true;
  const {model,features}=currentInput();
  document.querySelector('#flow-input').textContent=`${Object.keys(features).length} survey fields; model selection: ${model}.${loadedReference?` Held-out record ${loadedReference.row_id}.`:''}`;
  document.querySelector('#flow-processing').textContent='Validating input and running selected models…';
  document.querySelector('#flow-output').textContent='Waiting for results.';
  const submit=document.querySelector('#submit'); submit.disabled=true; submit.textContent='Running…';
  document.querySelector('#results').replaceChildren(paragraph('muted','Running selected models…'));
  try {
    const data=await readJSON('/api/predict',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({model,features})});
    lastFeatures=features;
    displayResults(data,referenceFor(features));
  } catch(error) {
    showError(error.message);
    document.querySelector('#flow-processing').textContent='The request did not complete.';
    document.querySelector('#flow-output').textContent=error.message;
    document.querySelector('#results').replaceChildren(paragraph('muted','Audit unavailable. Check the form error.'));
  } finally {submit.disabled=false; submit.textContent='Run audit';}
}
form.addEventListener('submit',async event=>{event.preventDefault();await runAudit();});

document.querySelector('#example').addEventListener('click',async()=>{
  errorBox.hidden=true;
  const button=document.querySelector('#example'); button.disabled=true; button.textContent='Loading…';
  try {
    const exclude=[...seenRows].join(',');
    const kind=document.querySelector('#sample-kind').value;
    const params=new URLSearchParams({kind}); if(exclude) params.set('exclude',exclude);
    const data=await readJSON(`/api/example?${params}`);
    if(data.reference) {
      if(seenRows.has(data.reference.row_id)) seenRows.clear();
      seenRows.add(data.reference.row_id);
      loadedReference=data.reference;
      document.querySelector('#sample-info').textContent=`Held-out record ${data.reference.row_id}; saved dataset label ${data.reference.actual_label}; case type: ${document.querySelector('#sample-kind').selectedOptions[0].textContent}.`;
    } else {
      loadedReference=null;
      document.querySelector('#sample-info').textContent='Training example loaded; held-out reference label is unavailable here.';
    }
    loadedFeatures=data.features;
    for(const [key,value] of Object.entries(data.features)) form.elements.namedItem(key).value=value;
    form.elements.namedItem('model').value='ALL';
    await runAudit();
  } catch(error) {showError(error.message);}
  finally {button.disabled=false; button.textContent='Load random record';}
});

document.querySelector('#sensitivity').addEventListener('click',async()=>{
  if(!lastFeatures) return;
  const button=document.querySelector('#sensitivity'); button.disabled=true; button.textContent='Checking…';
  try {
    const report=await readJSON('/api/audit/sensitivity',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({features:lastFeatures})});
    document.querySelector('#sensitivity-summary').textContent=`${report.variations_tested} one-field changes tested. Label flips: ML ${report.flip_counts.ML}, DL ${report.flip_counts.DL}, QML ${report.flip_counts.QML}.`;
    const body=document.querySelector('#sensitivity-body'); body.replaceChildren();
    if(!report.changes.length) {
      const row=document.createElement('tr'); const item=cell('No label changes in the tested variations.'); item.colSpan=3; row.append(item); body.append(row);
    }
    for(const change of report.changes) {
      const row=document.createElement('tr');
      for(const value of [change.field,change.tested_value,change.changed_models.join(', ')]) row.append(cell(value));
      body.append(row);
    }
  } catch(error) {showError(error.message);}
  finally {button.disabled=false; button.textContent='Check one-field changes';}
});

async function initialize(){
  try {await readJSON('/health/ready');document.querySelector('#health').textContent='Models ready';}
  catch {document.querySelector('#health').textContent='Models unavailable';}
  try {
    const data=await readJSON('/api/audit');
    document.querySelector('#audit-summary').textContent=`${data.source_rows} source records → ${data.clean_rows} clean records → ${data.test_count} held-out records (${data.test_labels.NO} NO, ${data.test_labels.YES} YES). Removed ${data.duplicates_removed} duplicates and ${data.conflicting_rows_excluded} conflicting rows.`;
    const errors=document.querySelector('#audit-errors'); errors.replaceChildren();
    for(const name of ['ML','DL','QML']) {
      const row=document.createElement('tr');
      for(const value of [name,data.models[name].true_negative,data.models[name].false_positive,data.models[name].false_negative,data.models[name].true_positive]) row.append(cell(value));
      errors.append(row);
    }
    if(data.agreement) {
      const a=data.agreement;
      document.querySelector('#summary-disagreements').textContent=`${a.disagreement_count} / ${data.test_count}`;
      document.querySelector('#summary-any-wrong').textContent=`${a.any_model_wrong_count} / ${data.test_count}`;
      document.querySelector('#summary-all-wrong').textContent=`${a.all_models_wrong_count} / ${data.test_count}`;
      document.querySelector('#audit-disagreement').textContent=`Pairwise label disagreements: ML–DL ${a.pairwise_disagreement.ML_DL}; ML–QML ${a.pairwise_disagreement.ML_QML}; DL–QML ${a.pairwise_disagreement.DL_QML}. Agreement alone does not establish correctness.`;
    }
    const slices=document.querySelector('#slice-body'); slices.replaceChildren();
    if(data.slices) for(const item of data.slices) {
      const row=document.createElement('tr');
      const format=name=>item.accuracy[name]===null?'—':`${(100*item.accuracy[name]).toFixed(1)}%`;
      for(const value of [`${item.dimension}: ${item.group}`,item.count,item.NO,item.YES,format('ML'),format('DL'),format('QML')]) row.append(cell(value));
      slices.append(row);
    }
  } catch(error) {document.querySelector('#audit-summary').textContent=error.message;}
  try {
    const data=await readJSON('/api/metrics');
    document.querySelector('#split-note').textContent=`${data.unique_rows} clean records; ${data.splits.train.count} train, ${data.splits.validation.count} validation, ${data.splits.test.count} test; seed ${data.seed}.`;
    document.querySelector('#baseline').textContent=`Always predicting the training majority class gives ${(100*data.majority_baseline_accuracy).toFixed(1)}% test accuracy. Balanced accuracy reveals minority-class performance.`;
    const body=document.querySelector('#metrics-body'); body.replaceChildren();
    for(const name of ['ML','DL','QML']) {
      const row=document.createElement('tr'); row.append(cell(name));
      for(const key of ['accuracy','balanced_accuracy','precision','recall','f1','roc_auc']) row.append(cell(`${(100*data.models[name][key]).toFixed(1)}%`));
      body.append(row);
    }
  } catch(error) {document.querySelector('#split-note').textContent=error.message;}
}
initialize();
