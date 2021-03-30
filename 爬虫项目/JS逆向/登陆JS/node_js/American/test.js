
var mjAPI = require("mathjax-node")
 mathjaxText = 'Global well-posedness for the $L^2$-critical Hartree  equation on $\mathbb{R}^n$, $n\ge 3$'
function MathJax2Xml(mathjaxFormula) {
  mjAPI.config({
  });
  mjAPI.start();
  mjAPI.typeset({
    math: mathjaxFormula,
    format: "TeX",
    mml: true
  }, function (data) {
    if (!data.errors) {
      console.log(data.mml);
    } else {
      console.log("<p>ERROR</p>");
    }
  });
}

var args = process.argv.splice(2);
MathJax2Xml(args[0])