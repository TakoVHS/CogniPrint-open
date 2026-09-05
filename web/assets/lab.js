(() => {
  const input = document.querySelector('[data-lab-input]');
  const metricsRoot = document.querySelector('[data-lab-metrics]');
  const vectorRoot = document.querySelector('[data-lab-vector]');
  const sample = document.querySelector('[data-lab-sample]');
  if (!input || !metricsRoot || !vectorRoot) return;

  const log2 = x => Math.log(x) / Math.log(2);
  const entropy = items => {
    if (!items.length) return 0;
    const counts = new Map();
    items.forEach(x => counts.set(x, (counts.get(x) || 0) + 1));
    let h = 0;
    counts.forEach(n => { const p = n / items.length; h -= p * log2(p); });
    return h;
  };
  const syllables = word => {
    const w = word.toLowerCase().replace(/[^a-z]/g, '');
    if (!w) return 0;
    const groups = w.replace(/e$/,'').match(/[aeiouy]+/g);
    return Math.max(1, groups ? groups.length : 1);
  };
  const fmt = n => Number.isFinite(n) ? n.toFixed(4) : '0.0000';

  function analyse(text) {
    const words = (text.match(/[\p{L}\p{N}’'-]+/gu) || []);
    const letters = (text.match(/\p{L}/gu) || []);
    const chars = [...text].filter(c => !/\s/u.test(c));
    const sentences = text.split(/[.!?]+/).map(s => s.trim()).filter(Boolean);
    const wordLower = words.map(w => w.toLowerCase());
    const uniq = new Set(wordLower);
    const bigrams = [];
    for (let i=0;i<chars.length-1;i++) bigrams.push(chars[i]+chars[i+1]);
    const counts = new Map();
    wordLower.forEach(w => counts.set(w,(counts.get(w)||0)+1));
    let simpson = 0;
    counts.forEach(n => { const p = n / Math.max(words.length,1); simpson += p*p; });
    const avgWord = words.length ? words.reduce((s,w)=>s+[...w].length,0)/words.length : 0;
    const ttr = words.length ? uniq.size/words.length : 0;
    const charEntropy = entropy(chars);
    const wordEntropy = entropy(wordLower);
    const punct = text.length ? (text.match(/[\p{P}]/gu)||[]).length/text.length : 0;
    const upper = letters.length ? (text.match(/\p{Lu}/gu)||[]).length/letters.length : 0;
    const avgSyll = words.length ? words.reduce((s,w)=>s+syllables(w),0)/words.length : 0;
    const bigramUniq = bigrams.length ? new Set(bigrams).size/bigrams.length : 0;
    const diversity = 1-simpson;
    const digits = words.length ? words.filter(w=>/\d/.test(w)).length/words.length : 0;
    const sentLen = sentences.length ? words.length/sentences.length : words.length;
    const syllTotal = words.reduce((s,w)=>s+syllables(w),0);
    const reading = words.length && sentences.length ? 206.835 - 1.015*(words.length/sentences.length) - 84.6*(syllTotal/words.length) : 0;
    return [avgWord,ttr,charEntropy,wordEntropy,punct,upper,avgSyll,bigramUniq,diversity,digits,sentLen,reading];
  }

  const labels = ['Mean word length','Type-token ratio','Character entropy','Word entropy','Punctuation ratio','Uppercase ratio','Mean syllables / word','Character-bigram uniqueness','Simpson diversity','Digit-token ratio','Mean sentence length','Reading ease'];
  function render() {
    const v = analyse(input.value);
    metricsRoot.innerHTML = labels.map((label,i)=>`<div class="lab-metric"><span>f${i+1} · ${label}</span><b>${fmt(v[i])}</b></div>`).join('');
    vectorRoot.textContent = `φ_lab(T) = [${v.map(fmt).join(', ')}]`;
  }
  input.addEventListener('input', render);
  if (sample) sample.addEventListener('click', () => { input.value = 'Mathematics becomes useful when a hypothesis can survive measurement, comparison, perturbation, and failure. CogniPrint treats language as an observable statistical object while preserving uncertainty about authorship and provenance.'; render(); });
  render();
})();