// export CLASSPATH=$CLASSPATH:"/Users/asif.hasan/Google Drive/RA/AMN/lib/AMANDA/*":"/Users/asif.hasan/Google Drive/RA/AMN/lib/LifeRay/*"

import java.util.zip.Inflater
import java.util.zip.Deflater
import java.security.Security
import javax.crypto.Cipher

// function providerExists
def providerExists(pName){
    return Security.providers.any { p ->
        p.getName() == pName
    }
}

// function decryptor
def decrypt(content, key, cipher) {
    Cipher localCipher = null

    if (providerExists("BC")) {
        localCipher = Cipher.getInstance(cipher, "BC")
    } else {
        localCipher = Cipher.getInstance(cipher)
    }

    localCipher.init(Cipher.DECRYPT_MODE, key)
    return localCipher.doFinal(content)
}

// function encryptor
def encrypt(content, key, cipher) {
    Cipher localCipher = null

    if (providerExists("BC")) {
        localCipher = Cipher.getInstance(cipher, "BC")
    } else {
        localCipher = Cipher.getInstance(cipher)
    }

    localCipher.init(Cipher.ENCRYPT_MODE, key)
    return localCipher.doFinal(content)
}

// function inflate
def inflate(contentBytes) {
    byte[] inflatedBytes = new byte[3000]
    inflater = new Inflater()

    inflater.setInput(contentBytes, 0, contentBytes.length)
    int inflatedSize = inflater.inflate(inflatedBytes)
    inflater.end()

    return inflatedBytes[0..<inflatedSize]
}

// function deflate
def deflate(contentBytes) {
    byte[] deflatedBytes = new byte[1000]
    deflater = new Deflater(Deflater.BEST_COMPRESSION, false)

    deflater.setInput(contentBytes, 0, contentBytes.length)
    deflater.finish();
    int deflatedSize = deflater.deflate(deflatedBytes)
    deflater.end()

    return deflatedBytes[0..<deflatedSize]
}
