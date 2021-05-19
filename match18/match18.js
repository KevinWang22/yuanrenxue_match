var CryptoJS = require('crypto-js');

function get_v(text, timestamp){
    text = CryptoJS["enc"].Utf8.parse(text);
    var key = CryptoJS["enc"].Utf8.parse(timestamp);

    var enc_result = CryptoJS["AES"].encrypt(text, key, {
        'mode': CryptoJS["mode"].CBC,
        'padding': CryptoJS["pad"].Pkcs7,
        'iv': key
    });

    return encodeURIComponent(enc_result.toString());

}
