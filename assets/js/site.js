(() => {
  'use strict';

  const menuButton = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.main-nav');
  if (menuButton && nav) {
    menuButton.addEventListener('click', () => {
      const open = menuButton.getAttribute('aria-expanded') === 'true';
      menuButton.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('is-open', !open);
    });
  }

  const demoForms = document.querySelectorAll('[data-demo-form]');
  demoForms.forEach((demoForm) => {
    demoForm.addEventListener('submit', (event) => {
      event.preventDefault();
      if (!demoForm.reportValidity()) return;
      const status = demoForm.querySelector('[data-demo-status]');
      if (status) {
        status.classList.add('is-visible');
        status.focus();
      }
    });
  });

  const form = document.querySelector('[data-quote-form]');
  if (!form) return;

  const material = form.querySelector('#material');
  const thickness = form.querySelector('#thickness');
  const width = form.querySelector('#width');
  const height = form.querySelector('#height');
  const quantity = form.querySelector('#quantity');
  const partsGroup = document.querySelector('[data-parts]');
  const output = {
    layout: document.querySelector('[data-layout]'),
    utilization: document.querySelector('[data-utilization]'),
    weight: document.querySelector('[data-weight]'),
    waste: document.querySelector('[data-waste]'),
    lead: document.querySelector('[data-lead]'),
    price: document.querySelector('[data-price]')
  };

  const decimal = (number, digits = 1) => new Intl.NumberFormat('az-AZ', {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits
  }).format(number);

  const clamp = (value, min, max) => Math.min(Math.max(value, min), max);

  function calculate() {
    const selected = material.options[material.selectedIndex];
    const density = Number(selected.dataset.density);
    const materialRate = Number(selected.dataset.rate);
    const t = clamp(Number(thickness.value) || 1, 0.8, 16);
    const w = clamp(Number(width.value) || 20, 20, 1450);
    const h = clamp(Number(height.value) || 20, 20, 2950);
    const count = clamp(Math.round(Number(quantity.value) || 1), 1, 500);
    const gap = 8;

    const normalCols = Math.max(1, Math.floor(3000 / (w + gap)));
    const normalRows = Math.max(1, Math.floor(1500 / (h + gap)));
    const rotatedCols = Math.max(1, Math.floor(3000 / (h + gap)));
    const rotatedRows = Math.max(1, Math.floor(1500 / (w + gap)));
    const normalCapacity = normalCols * normalRows;
    const rotatedCapacity = rotatedCols * rotatedRows;
    const rotated = rotatedCapacity > normalCapacity;
    const cols = rotated ? rotatedCols : normalCols;
    const rows = rotated ? rotatedRows : normalRows;
    const capacity = cols * rows;
    const sheets = Math.ceil(count / capacity);
    const partArea = (w * h) / 1_000_000;
    const totalArea = partArea * count;
    const sheetArea = 4.5 * sheets;
    const utilization = clamp((totalArea / sheetArea) * 100, 0, 100);
    const weight = totalArea * (t / 1000) * density * 1000;
    const perimeterM = ((w + h) * 2 / 1000) * count;
    const cutRate = 0.16 + t * 0.035;
    let estimate = weight * materialRate + perimeterM * cutRate + sheets * 7.5 + 18;
    if (form.elements.deburr.checked) estimate += count * 0.45;
    if (form.elements.bend.checked) estimate += count * 1.8;
    if (form.elements.coat.checked) estimate += totalArea * 2 * 7.5;
    const lower = Math.max(25, Math.round(estimate * .92));
    const upper = Math.round(estimate * 1.10);
    const lead = count <= 30 ? 2 : count <= 100 ? 3 : count <= 250 ? 5 : 7;

    output.layout.textContent = `${cols} × ${rows} / ${sheets} sac`;
    output.utilization.textContent = `${decimal(utilization)}%`;
    output.weight.textContent = `${decimal(weight)} kg`;
    output.waste.textContent = `${decimal(100 - utilization)}%`;
    output.lead.textContent = `${lead} iş günü`;
    output.price.textContent = `${lower}–${upper} ₼`;

    drawParts({ w, h, count: Math.min(count, capacity), cols, rows, rotated });
  }

  function drawParts({ w, h, count, cols, rotated }) {
    const ns = 'http://www.w3.org/2000/svg';
    const marginX = 30;
    const marginY = 22;
    const usableWidth = 548;
    const usableHeight = 304;
    const partW = (rotated ? h : w) / 3000 * usableWidth;
    const partH = (rotated ? w : h) / 1500 * usableHeight;
    const gapX = Math.min(4, Math.max(1.2, (usableWidth - cols * partW) / Math.max(cols, 1)));

    partsGroup.replaceChildren();
    const visible = Math.min(count, 120);
    for (let index = 0; index < visible; index += 1) {
      const col = index % cols;
      const row = Math.floor(index / cols);
      const rect = document.createElementNS(ns, 'rect');
      rect.setAttribute('class', 'part');
      rect.setAttribute('x', String(marginX + col * (partW + gapX)));
      rect.setAttribute('y', String(marginY + row * (partH + gapX)));
      rect.setAttribute('width', String(Math.max(2, partW)));
      rect.setAttribute('height', String(Math.max(2, partH)));
      rect.setAttribute('rx', '1');
      partsGroup.append(rect);
    }
  }

  form.addEventListener('input', calculate);
  form.addEventListener('change', calculate);
  calculate();
})();
