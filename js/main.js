const container = document.getElementById('poems');
const nav = document.getElementById('category-nav');

let allPoems = [];

function stripYaml(text) {
  if (text.startsWith('---')) {
    const parts = text.split('---');
    if (parts.length >= 3) {
      return parts.slice(2).join('---').trim();
    }
  }
  return text;
}

function renderPoems(filteredPoems) {
  container.innerHTML = '';
  filteredPoems.forEach(poem => {
    fetch(poem.file)
      .then(res => res.text())
      .then(text => {
        const cleanText = stripYaml(text);
        const poemDiv = document.createElement('div');
        poemDiv.className = 'poem';

        const content = document.createElement('div');
        content.className = 'poem-content';
        content.innerHTML = marked.parse(cleanText);

        if (poem.tags && poem.tags.length > 0) {
          const tagsDiv = document.createElement('div');
          tagsDiv.className = 'poem-tags';
          poem.tags.forEach(tag => {
            const span = document.createElement('span');
            span.className = 'tag';
            span.textContent = tag;
            tagsDiv.appendChild(span);
          });
          poemDiv.appendChild(tagsDiv);
        }

        poemDiv.appendChild(content);
        container.appendChild(poemDiv);
      });
  });
}

function buildNav(poems) {
  const tags = new Set(['All']);
  poems.forEach(p => p.tags.forEach(t => tags.add(t)));
  
  nav.innerHTML = '';
  tags.forEach(tag => {
    const btn = document.createElement('button');
    btn.textContent = tag;
    btn.className = 'nav-btn';
    btn.onclick = () => {
      const filtered = tag === 'All' ? poems : poems.filter(p => p.tags.includes(tag));
      renderPoems(filtered);
    };
    nav.appendChild(btn);
  });
}

function init() {
  fetch('poems.json')
    .then(res => res.json())
    .then(poems => {
      allPoems = poems;
      buildNav(poems);
      renderPoems(poems);
    })
    .catch(err => {
      console.error('Error:', err);
      container.innerHTML = '<p>The collection is being prepared...</p>';
    });
}

document.addEventListener('DOMContentLoaded', init);
