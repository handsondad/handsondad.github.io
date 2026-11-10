import { build } from "esbuild";
import { statSync } from "node:fs";
import { fileURLToPath } from "node:url";

const outfile = fileURLToPath(new URL("../../assets/js/home-duo.js", import.meta.url));

await build({
  entryPoints: [fileURLToPath(new URL("src/home-duo.js", import.meta.url))],
  bundle: true,
  format: "esm",
  minify: true,
  target: "es2020",
  legalComments: "eof",
  banner: { js: "/* 由 tools/home-duo 生成，请勿手改。three.js © three.js authors, MIT License. */" },
  outfile
});

const kb = statSync(outfile).size / 1024;
console.log(`assets/js/home-duo.js ${kb.toFixed(0)} KB`);
if (kb > 800) throw new Error(`打包体积 ${kb.toFixed(0)} KB 超出预期，检查是否误引入了多余模块`);
