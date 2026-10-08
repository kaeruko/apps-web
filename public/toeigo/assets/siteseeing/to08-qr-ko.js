(() => {
  'use strict';
  // QR codes are only needed on the printable flyer, not on the LP.
  if (!document.documentElement.classList.contains('flyer-mode')) return;
  // Store URLs represented by precomputed QR modules, including quiet zones.
  const codes = {
    'qr-ios': [
      "00000000000","00000000000","00000000000","00000000000","0fe7ae23f80","082fe08a080",
      "0baad1f2e80","0bac875ae80","0ba6d552e80","0824e802080","0feaaaabf80","000c21b0000",
      "082b7e3e700","0cd71318e00","07b116e4b00","08d1a119f00","067d7b3a080","0a5fad3b180",
      "042824c6700","04c310b5280","026a4c35880","0e819bb2680","03fa9599680","05cb438ef80",
      "086b9f8dd80","09cd6d90c00","0b6f1e40f00","0950408de00","0df8d98fd00","000dfd58a80",
      "0fe73adab00","0820d038e80","0ba4c28fd00","0ba5cb6df80","0ba28bd9980","08271a13e00",
      "0fec463f100","00000000000","00000000000","00000000000","00000000000"
    ],
    'qr-android': [
      "000000000000","000000000000","000000000000","000000000000","0fefcb0bbf80","082036c0a080",
      "0ba497cb2e80","0bac318fae80","0baa8a73ae80","082f93e6a080","0feaaaaabf80","000cfe2a0000",
      "08bfb3397c80","05944d978d00","0a23aadf4600","0a5886625f00","0fb21d796780","0bd8be1f8c00",
      "05ab9a7f3e00","018f105a3a00","022959987600","0c9e4373cf00","09b8f71bba00","0245bdd94300",
      "0536c4787200","0912fa739800","0726149ffe00","0918fe2a5a80","07f75333f700","0d01e99fca00",
      "03b2eeb3cc00","0103c67a1a80","0efa55fbfe80","000a7c168900","0feed2fea900","0826f9c18e80",
      "0bad2888fe80","0ba323337080","0ba577572600","08249dd14f00","0feb64d85380","000000000000",
      "000000000000","000000000000","000000000000"
    ]
  };

  for (const [id, rows] of Object.entries(codes)) {
    const canvas = document.getElementById(id);
    if (!(canvas instanceof HTMLCanvasElement)) throw new Error('QR canvas missing: ' + id);
    const size = rows.length;
    if (rows.some(row => row.length !== Math.ceil(size / 4) || !/^[0-9a-f]+$/.test(row))) {
      throw new Error('Invalid QR module data: ' + id);
    }
    const scale = 8;
    canvas.width = size * scale;
    canvas.height = size * scale;
    const context = canvas.getContext('2d');
    if (!context) throw new Error('QR canvas 2D context unavailable: ' + id);
    context.fillStyle = '#ffffff';
    context.fillRect(0, 0, canvas.width, canvas.height);
    context.fillStyle = '#111827';
    for (let y = 0; y < size; y++) {
      for (let x = 0; x < size; x++) {
        const nibble = Number.parseInt(rows[y][Math.floor(x / 4)], 16);
        if (nibble & (8 >> (x % 4))) {
          context.fillRect(x * scale, y * scale, scale, scale);
        }
      }
    }
  }
})();
