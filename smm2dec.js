var myArgs = process.argv.slice(2);
const { encryption, Course } = require('partrick');
const fs = require('fs');

switch (myArgs[0]) {


case '-d':
    const encrypted_data = fs.readFileSync(myArgs[1]);

    const decrypted = encryption.decryptCourse(encrypted_data);

    fs.writeFileSync(myArgs[2], decrypted);
    break;

case '-e':
    const decrypted_data = fs.readFileSync(myArgs[1]);

    const encrypted = encryption.encryptCourse(decrypted_data);

    fs.writeFileSync(myArgs[2], encrypted);
    break;

default:
    console.log('Usage: ' + __filename + ' input output');
    console.log('flag -d decrypt');
    console.log('flag -e encrypt');
}