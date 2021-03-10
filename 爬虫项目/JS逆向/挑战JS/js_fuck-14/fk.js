window=global
CryptoJS = require("crypto-js")

var url = "/api/challenge14";

call = function(num) {
    window.num = num;
    console.log(window.num);
    window.k = 'wdf2ff*TG@*(F4)*YH)g430HWR(*)' + 'wse';
    window.t = Date.parse(new Date()) / 1000;
    // window.t ="1615361190"
    console.log(window.t);
    window.m = CryptoJS.enc.Utf8.parse(window.k);
    window.a = function (word) {
        console.log(word)
        var srcs = CryptoJS.enc.Utf8.parse(word);
        console.log(srcs)
        var encrypted = CryptoJS.AES.encrypt(srcs, window.m, {
            mode: CryptoJS.mode.ECB,
            padding: CryptoJS.pad.Pkcs7
        });
        console.log( encrypted.toString())
        return encrypted.toString();
    };
    window.s = window.a(window.t + '|' + window.num)
return window.s
};
call(2)