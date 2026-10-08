(() => {
'use strict';
if (!document.documentElement.classList.contains('flyer-mode')) return;
const locale = document.documentElement.lang.toLowerCase();
const language = locale.startsWith('zh') ? 'zh' : locale.startsWith('en') ? 'en' : null;
if (!language) throw new Error('Unsupported QR locale: ' + locale);
const QR = {
  en: {
    ios: "00000000000,00000000000,00000000000,00000000000,0fed4393f80,082e4612080,0ba40a9ae80,0baabfbae80,0ba7638ae80,0824232a080,0feaaaabf80,000f8728000,0b752552580,0b59abfb680,0fec203fd80,05536a35400,00b7168cd00,08160ba1700,057abfabc00,0b090856a00,05697aeee00,0240529ed80,0731f82fb00,0f8a6514900,07fd44e0680,0ac35173480,00648e9b980,05c68ba1500,0a2bd43f880,000c7bc8c00,0fe9e1ba800,082ee8d8e00,0ba0745fb80,0bab4041480,0bade66f400,08229e89880,0fecfd52a00,00000000000,00000000000,00000000000,00000000000",
    android: "000000000000,000000000000,000000000000,000000000000,0fe2aaccbf80,08245f0fa080,0baf19f3ae80,0baebfb72e80,0baafbb4ae80,082d8221a080,0feaaaaabf80,000f30128000,0be102fe3e00,06d89c509100,00f0a4e7a580,02930842bc80,0aae6cae7b80,0cc0cfd89000,09285447dd80,010ede62d980,00fb485f6a00,08d132b4d300,036279235980,0a86b3e1a080,022bb5bf6e00,060ecbb48400,03a5baa71d80,011b5012b900,052362f4eb00,085d3858d600,0b61e08b2f80,0bc14842f900,0bf6243cfa80,000e4dd18d00,0fe71cc6aa80,082f37f98d00,0ba9194ffa80,0bad72f46c80,0baef96fc580,082793e9ac80,0fee151f4f80,000000000000,000000000000,000000000000,000000000000"
  },
  zh: {
    ios: "00000000000,00000000000,00000000000,00000000000,0fe74393f80,082270ca080,0baa51f2e80,0babbfbae80,0baed552e80,0828f842080,0feaaaabf80,000a31f0000,0be77e3be00,0d08abfb680,05a116e4b00,0bc4b158f00,02a7168cd00,035bfd7a180,0ca864c6700,07cd4856a00,0fa60c35880,089709f3680,0629f82fb00,07d653cff80,087b9f8dd80,0ac35173480,0b2b7840f00,08d472cce00,0ae3f43f880,000b6d18a80,0fe6badab00,082ee8d8e00,0badc28fd00,0baddb2cf80,0ba9c46f400,08276852e00,0feea63f100,00000000000,00000000000,00000000000,00000000000",
    android: "000000000000,000000000000,000000000000,000000000000,0fe9c99bbf80,08252748a080,0ba2a6532e80,0bae108fae80,0bacb673ae80,082b2da6a080,0feaaaaabf80,0008704a0000,08bfb9b97c80,04c787378d00,0dabd3574600,0e15ffe25f00,027bcc796780,0fcb1a1f8c00,0dae3c5f3e00,0191767a3a00,0ce5b3307600,0101e9f3cf00,0f6ece9bba00,0c8684594300,0266d5787200,07941e339800,0bbb529ffe00,0085b84a5a80,07a0d993f700,0b50431fca00,03f35733cc00,039fdffa1b80,0d6224fbff80,000c78568900,0fed549ea900,0821bfa18e80,0ba9c228fe80,0ba209937080,0ba68ed72600,0825a4514f00,0fe995d85380,000000000000,000000000000,000000000000,000000000000"
  }
};
for (const [id,key] of [['qr-ios','ios'],['qr-android','android']]) {
  const canvas = document.getElementById(id);
  if (!(canvas instanceof HTMLCanvasElement)) throw new Error('QR canvas missing: ' + id);
  const rows = QR[language][key].split(',');
  const size = rows.length;
  if (!rows.every(row => row.length === Math.ceil(size/4) && /^[0-9a-f]+$/.test(row))) {
    throw new Error('Invalid precomputed QR data for ' + language + ':' + key);
  }
  const scale=8,ctx=canvas.getContext('2d');
  if (!ctx) throw new Error('QR canvas unavailable: '+id);
  canvas.width=size*scale;canvas.height=size*scale;
  ctx.fillStyle='#fff';ctx.fillRect(0,0,canvas.width,canvas.height);
  ctx.fillStyle='#111827';
  for(let y=0;y<size;y++)for(let x=0;x<size;x++){
    const nibble=parseInt(rows[y][Math.floor(x/4)],16);
    if(nibble&(8>>(x%4)))ctx.fillRect(x*scale,y*scale,scale,scale);
  }
}
})();