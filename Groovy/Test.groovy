import java.security.Key
import java.security.Provider
import java.security.Security
import java.security.KeyFactory
import javax.crypto.spec.SecretKeySpec
import java.security.spec.X509EncodedKeySpec
import java.security.spec.PKCS8EncodedKeySpec

import com.alphinat.interview.si.encoding.Base64Util
import com.alphinat.interview.si.security.CryptoUtil

// literals etc.
publicKey = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhSO2mh+ql9fA850zd4WiMprQfY4l+Rtvo+yVkxKGVGX8028uBB8/TFIv4gDZSGTp36DJNSQ+U27eXOXeB3mMRry66Nn/+TPo3q/+k2Vkk+kBiWsXBVv9FWN94PRnD2dsTlVOuqWTPyF11D8Pwbma5oLymTY4bSqJoAwNB1Fvhuw5a616HPUeP/heACrmmomXv+oyOYbgTfjxixkhOh5NCjGZmhk8tgITy+f7tpWzjr2EsG0MlUbhlm5u+iUzH+9DwdodK04F46QdjeBRcnePdTFYbZQZ6GBLveLp7yb4YxFAFq5XcK5knvFWjROaHWtHUzS2fnsr5yp+lfVEoIMgxwIDAQAB"
scriptDir = new File(getClass().protectionDomain.codeSource.location.path).parent
filePath = scriptDir + "/files/"

// load utilities
GroovyShell shell = new GroovyShell()
def utils = shell.parse(new File(scriptDir + "/Utils.groovy"))

// Security provider
localProvider = Class.forName("org.bouncycastle.jce.provider.BouncyCastleProvider").newInstance()
Security.addProvider(localProvider);

// read license file
fName = String.format("$filePath/smartguide.lic", filePath)
byte[] licBytes = new File(fName).getBytes()

// decryption key
if (utils.providerExists("BC")) {
    println "Using BC Provider"
    cipher = "RSA/NONE/PKCS1Padding";
    localKeyFactory = KeyFactory.getInstance("RSA", "BC");
} else {
    println "Using Default Provider"
    cipher = "RSA";
    localKeyFactory = KeyFactory.getInstance("RSA");
}

byte[] b = Base64Util.decode(this.publicKey)
X509EncodedKeySpec localX509EncodedKeySpec = new X509EncodedKeySpec(b)
localPublicKey = localKeyFactory.generatePublic(localX509EncodedKeySpec)

//PKCS8EncodedKeySpec localPKCS8keySpec = new PKCS8EncodedKeySpec(b)
//localPrivateKey = localKeyFactory.generatePrivate(localPKCS8keySpec)

//Key rsaKey = new SecretKeySpec(b, "RSA");
//localPrivateKey = localKeyFactory.generatePrivate(localPKCS8keySpec)

/*
The flow is
decrypt -> inflate -> change -> deflate -> encrypt
*/

// divide into chunks
numChunks = licBytes.length / 256
licByteChunks = []
(0..<numChunks).collect().each { i ->
    byte[] c = licBytes[i*256..i*256+255]
    licByteChunks.add(c)
}

// decrypt chunks and merge
ByteArrayOutputStream outputStream = new ByteArrayOutputStream()
byte[] decryptedLicBytes = []
licByteChunks.each{ c ->
    byte[] d = utils.decrypt(c, localPublicKey, cipher)
    outputStream.write(d);
}
decryptedLicBytes = outputStream.toByteArray()

fName = String.format("$filePath/decrypted-compressed.lic", filePath)
new File(fName).withOutputStream { os ->
    os.write decryptedLicBytes
}

// encrypt chunks
byte[] reEncryptedLicBytes = utils.encrypt(decryptedLicBytes[0..<256] as byte[], localPublicKey, cipher)
//cryptoUtil = new CryptoUtil()
//reEncryptedLicBytes = cryptoUtil.encryptPKI(rsaKey, decryptedLicBytes[0..<256])

/*
// decompress
byte[] inflatedLicBytes = utils.inflate(decryptedLicBytes)
println inflatedLicBytes.length

// compress
byte[] deflatedLicBytes = utils.deflate(inflatedLicBytes)
println deflatedLicBytes.length

fName = String.format("$filePath/decrypted-compressed-decompressed.lic", filePath)
new File(fName).withOutputStream { os ->
    os.write deflatedLicBytes
}


//licenseText = new String(inflatedLicBytes);
//print licenseText
*/
