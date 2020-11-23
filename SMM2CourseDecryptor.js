const { encryption } = require("partrick");
const fs = require("fs");

var args = process.argv.slice(2);

function main() {
    if(args.length==2) {
        if(fs.statSync(args[0]).size.toString(16).toUpperCase()=="5C000") { // Encrypted Course Data
            console.log("Decrypting Course Data...")
            const encrypted = fs.readFileSync(args[0]);
            const decrypted = encryption.decryptCourse(encrypted);
            fs.writeFileSync(args[0], decrypted);
        }
        else if(fs.statSync(args[0]).size.toString(16).toUpperCase()=="5BFC0") { // Decrypted Course Data
            console.log("Encrypting Course Data...")
            const decrypted = fs.readFileSync(args[0]);
            const encrypted = encryption.encryptCourse(decrypted);
            fs.writeFileSync(args[0], encrypted);
        }
    } else {
        if(args.length==1) {
            if(fs.statSync(args[0]).size.toString(16).toUpperCase()=="5C000") { // Encrypted Course Data
                console.log("Decrypting Course Data...")
                const encrypted = fs.readFileSync(args[0]);
                const decrypted = encryption.decryptCourse(encrypted);
                fs.writeFileSync(args[0], decrypted);
            }
            else if(fs.statSync(args[0]).size.toString(16).toUpperCase()=="5BFC0") { // Decrypted Course Data
                console.log("Encrypting Course Data...")
                const decrypted = fs.readFileSync(args[0]);
                const encrypted = encryption.encryptCourse(decrypted);
                fs.writeFileSync(args[0], encrypted);
            }
        } else {
            console.log("Usage: "+__filename+" <input> [output]");
            return 0;
        }
    }
}

main();
console.log("Done!");