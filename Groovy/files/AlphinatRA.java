import com.csdc.amanda.smartguide.portal.EncryptionService;
import com.csdc.amanda.smartguide.portal.EncryptionException;
import com.alphinat.sgs.smartlet.ProcessSmartlet;
import com.alphinat.sgs.smartlet.ProcessSmartlet.APNLicenseLibrary;
import com.alphinat.interview.si.xml.Resolver;
import com.alphinat.interview.si.encoding.Base64Util;
import com.alphinat.interview.si.io.IOUtil;
import java.security.spec.X509EncodedKeySpec;
import java.util.Arrays;
import java.security.*;
import java.security.spec.*;
import javax.crypto.*;
import java.util.zip.*;
import java.io.*;
import javax.xml.transform.stream.StreamSource;

public class AlphinatRA
{
	public static void main(String[] args) {

		//System.out.println("Hello, World");

		//ProcessSmartlet ps =new ProcessSmartlet();

		//ProcessLicense();
		//EncryptLicense();
		ProcessDecryptEncrypt();
    }

	public static void EncryptLicense()
	{
		//String xml=GetXML();

		//System.out.println(xml);

		//byte[] arrayOfByte4;

		String xml="";//GetXMLFromEncryptedLicense();
		//xml =xml.substring(0, 1000);
		//xml="chudir bhai 1";
		xml+=xml;
		
		String licFileName = null;
		licFileName = "D:\\Apps\\Java\\Decompile\\files\\test.txt";
		licFileName = "D:\\Apps\\Java\\Decompile\\files\\test1.txt";
		licFileName = "D:\\Apps\\Java\\Decompile\\files\\smartguide1.txt";

		Resolver resolver = new Resolver();

		byte[] arrayOfByte4= null;

		arrayOfByte4= resolver.resolveBytes(licFileName, null);

		InputStream targetStream = new ByteArrayInputStream(xml.getBytes());
		//IOUtil u = new IOUtil();
		StreamSource localStreamSource=null;
		//localStreamSource.getInputStream();

		try
		{
			arrayOfByte4 = IOUtil.loadBytes(targetStream);//
			arrayOfByte4= resolver.resolveBytes(licFileName, null);
		}
		catch(IOException e)
		{
			e.printStackTrace();
		}

		//arrayOfByte4 = Base64Util.decode(xml);//not working

		//System.out.println(xml);
		//System.out.println(new String(arrayOfByte4));
		//System.out.println(arrayOfByte4);

		System.out.println("arrayOfByte4.length:"+arrayOfByte4.length);

		byte[] arrayOfByte3 = enCompressData(arrayOfByte4);

		System.out.println("arrayOfByte3.length:"+arrayOfByte3.length);
		//System.out.println(new String(arrayOfByte3));
		System.out.println(arrayOfByte3);


		byte[] arrayOfByte5 = GetEncryptedArray(arrayOfByte3);

		System.out.println("arrayOfByte5.length:"+arrayOfByte5.length);
		System.out.println(new String(arrayOfByte5));

		byte[] arrayOfByte51 = deCompressData(arrayOfByte3);

		System.out.println("arrayOfByte51.length:"+arrayOfByte51.length);

		String ss = new String(arrayOfByte51);
		System.out.println(ss);

		try
		{
			//WriteToFile(new String(arrayOfByte5));
			WriteToFile(arrayOfByte5);
		}
		catch (IOException e) {System.out.println(e); }


	}

	public static byte[] GetEncryptedArray(byte[] arrayOfByte3)
	{

		ProcessSmartlet ps =new ProcessSmartlet();
		ProcessSmartlet.APNLicenseLibrary li =ps.new APNLicenseLibrary("");

		String str = null;
		KeyFactory localKeyFactory = null;
		try
		{

			//str = "RSA/NONE/PKCS1Padding";
			//localKeyFactory = KeyFactory.getInstance("RSA", "BC");

			str = "RSA";
			localKeyFactory = KeyFactory.getInstance("RSA");
		}
		catch (NoSuchAlgorithmException e)
		{
		  //e.printStackTrace();
		  System.out.println(e); 
		}
		/*
		catch (NoSuchProviderException e)
		{
		  e.printStackTrace();
		}
		*/
		//String publicKey="";
		String publicKey = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhSO2mh+ql9fA850zd4WiMprQfY4l+Rtvo+yVkxKGVGX8028uBB8/TFIv4gDZSGTp36DJNSQ+U27eXOXeB3mMRry66Nn/+TPo3q/+k2Vkk+kBiWsXBVv9FWN94PRnD2dsTlVOuqWTPyF11D8Pwbma5oLymTY4bSqJoAwNB1Fvhuw5a616HPUeP/heACrmmomXv+oyOYbgTfjxixkhOh5NCjGZmhk8tgITy+f7tpWzjr2EsG0MlUbhlm5u+iUzH+9DwdodK04F46QdjeBRcnePdTFYbZQZ6GBLveLp7yb4YxFAFq5XcK5knvFWjROaHWtHUzS2fnsr5yp+lfVEoIMgxwIDAQAB";

		byte[] arrayOfByte1 = Base64Util.decode(publicKey);
		X509EncodedKeySpec localX509EncodedKeySpec = new X509EncodedKeySpec(arrayOfByte1);

		PublicKey localPublicKey = null;

		try
		{
			localPublicKey = localKeyFactory.generatePublic(localX509EncodedKeySpec);
		}
		catch (InvalidKeySpecException e)
		{
		  //e.printStackTrace();
		  System.out.println(e); 
		}

		int i = 0;
		int j = 245;//for encryption it should be 245
		int k = 0;
		byte[] arrayOfByte2 = new byte[j];
		byte[] licBytes = new byte[arrayOfByte3.length];
		Arrays.fill(licBytes, (byte)0);


		for (int m = 0; m < arrayOfByte3.length / j; m++)
		{
			i++;
			System.arraycopy(arrayOfByte3, m * j, arrayOfByte2, 0, j);
			byte[] arrayOfByte5 = null;

			try
			{
				arrayOfByte5 = encrypt(arrayOfByte2, localPublicKey, str);
			}
			catch (Exception e)
			{
			  //e.printStackTrace();
			  System.out.println(e); 
			}

			System.arraycopy(arrayOfByte5, 0, licBytes, k, arrayOfByte5.length);
			k += arrayOfByte5.length;
		}

		return licBytes;

	}

    public static void ProcessLicense()
    {

		String xml = "";

		xml = GetXMLFromEncryptedLicense("smartguide.lic");

		System.out.println(xml);

	}
    
    public static void ProcessDecryptEncrypt()
    {

		String xml = "";
		byte[] decryptedByte = GetXMLBytesFromEncryptedLicense("smartguide.lic");
		
		byte[] encryptedByte = GetEncryptedLicenseBytesFromXMLByte(decryptedByte);

		byte[] decryptedByte2 = GetXMLBytesFromEncryptedLicenseByte(encryptedByte);
		
		xml = new String(decryptedByte);

		System.out.println(xml);

	}
    
    
	private static byte[] encrypt(byte[] paramArrayOfByte, PublicKey paramPublicKey, String paramString) throws Exception
    {
		Cipher localCipher = null;
		//localCipher = Cipher.getInstance(paramString, "BC");
		localCipher = Cipher.getInstance(paramString);

		localCipher.init(Cipher.ENCRYPT_MODE, paramPublicKey);
		return localCipher.doFinal(paramArrayOfByte);

    }

	private static byte[] decrypt(byte[] paramArrayOfByte, PublicKey paramPublicKey, String paramString) throws Exception
    {
		Cipher localCipher = null;
		//localCipher = Cipher.getInstance(paramString, "BC");
		localCipher = Cipher.getInstance(paramString);

		localCipher.init(2, paramPublicKey);
		return localCipher.doFinal(paramArrayOfByte);

    }

	  public static byte[] compress(byte[] data) throws IOException {  

		   Deflater deflater = new Deflater();  

		   deflater.setInput(data);  

		   ByteArrayOutputStream outputStream = new ByteArrayOutputStream(data.length);   

		   deflater.finish();  

		   byte[] buffer = new byte['\u00C8'];   

		   while (!deflater.finished()) {  

		    int count = deflater.deflate(buffer); // returns the generated code... index  

		    outputStream.write(buffer, 0, count);   

		   }  

		   outputStream.close();  

		   byte[] output = outputStream.toByteArray();  

			System.out.println("compress. data.length:" + data.length);
			System.out.println("compress. output.length:" + output.length);

		   return output;  

		  }  

		  public static byte[] decompress(byte[] data) throws IOException, DataFormatException {  

		   Inflater inflater = new Inflater();   

		   inflater.setInput(data);  

		   ByteArrayOutputStream outputStream = new ByteArrayOutputStream(data.length);  

		   byte[] buffer = new byte['\u00C8'];  

		   while (!inflater.finished()) {  

		    int count = inflater.inflate(buffer);  

		    outputStream.write(buffer, 0, count);  

		   }  

		   outputStream.close();  

		   byte[] output = outputStream.toByteArray();  

			System.out.println("decompress. data.length:" + data.length);
			System.out.println("decompress. output.length:" + output.length);

			return output;  

		  }  

		 

    private static byte[] enCompressData(byte[] inBytes)
    {
		Deflater compresser = new Deflater();
		compresser.setInput(inBytes);
		ByteArrayOutputStream localByteArrayOutputStream = new ByteArrayOutputStream(inBytes.length);
		byte[] output = new byte[1024];

		System.out.println("enCompressData. inBytes.length:" + inBytes.length);

		//byte[] arrayOfByte1 = new byte['\u00C8'];//\u00C8
		byte[] bufferBytes = new byte['\u00C8'];//\u00C8
		
		System.out.println("	enCompressData. bufferBytes.length:" + bufferBytes.length);

		compresser.finish();

		
		while (!compresser.finished())
		{
			int i = compresser.deflate(bufferBytes);
			localByteArrayOutputStream.write(bufferBytes, 0, i);
			//System.out.println(i);
			//compresser.finish();

		}
		
		/*
		int compressedDataLength = compresser.deflate(output);
		compresser.end();
		System.out.println("enCompressData. compressedDataLength:" + compressedDataLength);
		localByteArrayOutputStream.write(output, 0, compressedDataLength);
		//System.out.println(arrayOfByte1.length);
		//return arrayOfByte1;
		
		*/
		try
		{
			localByteArrayOutputStream.close();
		}
		catch(IOException  e)
		{
			
		}
		
		byte[] outBytes=localByteArrayOutputStream.toByteArray();
		
		System.out.println("enCompressData. outBytes.length:" + outBytes.length);

		return outBytes;

		/*
		System.out.println(arrayOfByte1.length);
		//compresser.finish();
		int compressedDataLength = compresser.deflate(arrayOfByte1);
		System.out.println(paramArrayOfByte.length);
		System.out.println(arrayOfByte1.length);
		return arrayOfByte1;
		*/

		/*
		//for (;;)
		for (int m = 0; m < 15; m++)
		{
			if (!compresser.finished()) {
				//try
				{
					int i = compresser.deflate(arrayOfByte1);
					System.out.println(arrayOfByte1.length);
					localByteArrayOutputStream.write(arrayOfByte1, 0, i);
				}
				//catch (DataFormatException localDataFormatException) {}
			}
		}

		try
		{
			localByteArrayOutputStream.close();
		}
		catch (IOException localIOException) {}

		byte[] arrayOfByte2 = localByteArrayOutputStream.toByteArray();
		return arrayOfByte2;
		*/
		/*

     // Compress the bytes
     byte[] output = new byte[100];
     Deflater compresser = new Deflater();
     compresser.setInput(input);
     compresser.finish();
     int compressedDataLength = compresser.deflate(output);

     // Decompress the bytes
     Inflater decompresser = new Inflater();
     decompresser.setInput(output, 0, compressedDataLength);
     byte[] result = new byte[100];
     int resultLength = decompresser.inflate(result);
     decompresser.end();
		*/
    }

    private static byte[] deCompressData(byte[] inBytes)
    {
		Inflater localInflater = new Inflater();
		localInflater.setInput(inBytes);
		ByteArrayOutputStream localByteArrayOutputStream = new ByteArrayOutputStream(inBytes.length);
		byte[] bufferBytes = new byte['\u00C8'];

		System.out.println("deCompressData. inBytes.length:"+inBytes.length);
		System.out.println("	deCompressData. bufferBytes.length:"+bufferBytes.length);

		//for (;;)
		//for (int m = 0; m < 14; m++)
		while (!localInflater.finished())
		{
			if (!localInflater.finished()) {
				try
				{
					int i = localInflater.inflate(bufferBytes);
					//System.out.println(i);
					localByteArrayOutputStream.write(bufferBytes, 0, i);
				}
				catch (DataFormatException localDataFormatException) {}
			}
		}

		try
		{
			localByteArrayOutputStream.close();
		}
		catch (IOException localIOException) {}

		byte[] outBytes = localByteArrayOutputStream.toByteArray();
		
		System.out.println("deCompressData. outBytes.length:"+outBytes.length);

		return outBytes;
    }

	public static String GetXMLFromEncryptedLicense(String fileName)
    {
		String xml="";

		
		byte[] decompressedArrayOfByte = GetXMLBytesFromEncryptedLicense(fileName);
		
		//WriteToFile(decompressedArrayOfByte,"smartguideB.txt");
		
		//--06. convert the arraybyte
		xml = new String(decompressedArrayOfByte);
		//System.out.println(xml);

		//WriteToFile(xml,"smartguideT.txt");

		return xml;
		/*
		*/

	}

	public static byte[] GetXMLBytesFromEncryptedLicense(String fileName)
    {

		String licFileName = null;
		//licFileName = "C:\\temp\\smartguide.lic";
		//licFileName = "C:\\temp\\samplefile2.txt";
		//licFileName = "C:\\temp\\smartguide3.lic";
		//licFileName = "D:\\Apps\\Java\\Decompile\\files\\smartguide.lic";
		//licFileName = "D:\\Apps\\Java\\Decompile\\files\\smartguide5.lic";
		licFileName = "D:\\Apps\\Java\\Decompile\\files\\" + fileName;

		//--01. Read the encrypted file and convert to byte array
		Resolver resolver = new Resolver();
		byte[] licBytes= resolver.resolveBytes(licFileName, null);

		

		//--05. decompress the decryted array byte
		byte[] decompressedArrayOfByte = GetXMLBytesFromEncryptedLicenseByte(licBytes);
		
		//WriteToFile(decompressedArrayOfByte,"smartguideB.txt");
		
		//--06. convert the arraybyte
		//xml = new String(decompressedArrayOfByte);
		//System.out.println(xml);

		//WriteToFile(xml,"smartguideT.txt");

		return decompressedArrayOfByte;
		/*
		*/

	}
	
	public static byte[] GetXMLBytesFromEncryptedLicenseByte(byte[] licBytes)
    {
		System.out.println("GetXMLBytesFromEncryptedLicenseByte. licBytes.length:"+licBytes.length);//768

		//System.out.println(Arrays.toString(licBytes));
		//System.out.println(new String(licBytes));
		//System.out.println("bytes = " + PrintBytes(licBytes));
		//System.out.println(licBytes.length);//768

		//ProcessSmartlet ps =new ProcessSmartlet();
		//ProcessSmartlet.APNLicenseLibrary li =ps.new APNLicenseLibrary("");

		//--02. Generate a KeyFactory (RSA)
		String str = null;
      	KeyFactory localKeyFactory = null;
      	try
      	{
			//str = "RSA/NONE/PKCS1Padding";
			//localKeyFactory = KeyFactory.getInstance("RSA", "BC");

			str = "RSA";
        	localKeyFactory = KeyFactory.getInstance("RSA");
		}
		catch (NoSuchAlgorithmException e)
		{
		  //e.printStackTrace();
		  System.out.println(e); 
		}
		/*
		catch (NoSuchProviderException e)
		{
		  e.printStackTrace();
		}
		*/
      	
      	
		//--03. Generate PublicKey
		String publicKey = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhSO2mh+ql9fA850zd4WiMprQfY4l+Rtvo+yVkxKGVGX8028uBB8/TFIv4gDZSGTp36DJNSQ+U27eXOXeB3mMRry66Nn/+TPo3q/+k2Vkk+kBiWsXBVv9FWN94PRnD2dsTlVOuqWTPyF11D8Pwbma5oLymTY4bSqJoAwNB1Fvhuw5a616HPUeP/heACrmmomXv+oyOYbgTfjxixkhOh5NCjGZmhk8tgITy+f7tpWzjr2EsG0MlUbhlm5u+iUzH+9DwdodK04F46QdjeBRcnePdTFYbZQZ6GBLveLp7yb4YxFAFq5XcK5knvFWjROaHWtHUzS2fnsr5yp+lfVEoIMgxwIDAQAB";
		byte[] publicKeyArrayOfByte = Base64Util.decode(publicKey);
		X509EncodedKeySpec localX509EncodedKeySpec = new X509EncodedKeySpec(publicKeyArrayOfByte);

		PublicKey localPublicKey = null;

      	try
      	{
			localPublicKey = localKeyFactory.generatePublic(localX509EncodedKeySpec);
		}
		catch (InvalidKeySpecException e)
		{
		  //e.printStackTrace();
		  System.out.println(e); 
		}

		//--04. Copy the encrypted license byte to another byte array by decrypting 256 byte at a time
		byte[] copiedLicBytes = new byte[licBytes.length];
      	Arrays.fill(copiedLicBytes, (byte)0);
      	
      	int i = 0;
		int j = 256;//256
		int k = 0;
		byte[] arrayOfByte2 = new byte[j];


		for (int m = 0; m < licBytes.length / j; m++)
      	{
			i++;
			System.arraycopy(licBytes, m * j, arrayOfByte2, 0, j);
			byte[] arrayOfByte5 = null;

			try
			{
				arrayOfByte5 = decrypt(arrayOfByte2, localPublicKey, str);
			}
			catch (Exception e)
			{
			  //e.printStackTrace();
			  System.out.println(e); 
			}

			System.arraycopy(arrayOfByte5, 0, copiedLicBytes, k, arrayOfByte5.length);
			k += arrayOfByte5.length;
			
			//WriteToFile(arrayOfByte2,"encrypted_" + m + ".txt");
			//WriteToFile(arrayOfByte5,"decrypted_" + m + ".txt");

		}
		
		System.out.println("GetXMLBytesFromEncryptedLicenseByte. copiedLicBytes.length:"+copiedLicBytes.length);//768
		
		
		//WriteToFile(copiedLicBytes,"decrypted.txt");
		
		//--05. decompress the decryted array byte
		byte[] decompressedArrayOfByte = deCompressData(copiedLicBytes);
		
		byte[] compressAgain = enCompressData(decompressedArrayOfByte);
		byte[] decompressedAgain = deCompressData(compressAgain);
		//WriteToFile(decompressedArrayOfByte2,"comreessed_1.txt");

		/*
		try
		{
			byte[] a1 = decompress(copiedLicBytes);
			byte[] a2 = compress(a1);
			byte[] a3 = decompress(a2);
			

		}
		catch(Exception e)
		{
			System.out.println("GetXMLBytesFromEncryptedLicenseByte. e:"+e);
		}
		
		*/
		//WriteToFile(decompressedArrayOfByte,"smartguideB.txt");
		
		//--06. convert the arraybyte
		//xml = new String(decompressedArrayOfByte);
		//System.out.println(xml);

		//WriteToFile(xml,"smartguideT.txt");

		System.out.println("GetXMLBytesFromEncryptedLicenseByte. decompressedArrayOfByte.length:"+decompressedArrayOfByte.length);//768

		return decompressedArrayOfByte;
		/*
		*/

	}

	public static byte[] GetEncryptedLicenseBytesFromXMLByte(byte[] decompressedArrayOfByte)
    {

		
		System.out.println("GetEncryptedLicenseBytesFromXMLByte. decompressedArrayOfByte.length:"+decompressedArrayOfByte.length);//768

		//--05. decompress the decryted array byte. Encompress the xml byte
		byte[] copiedLicBytes = enCompressData(decompressedArrayOfByte);

		System.out.println("GetEncryptedLicenseBytesFromXMLByte. copiedLicBytes.length:"+copiedLicBytes.length);//768


		//byte[] licBytes= new byte[copiedLicBytes.length];
		byte[] licBytes= new byte[768];
		
		//System.out.println(Arrays.toString(licBytes));
		//System.out.println(new String(licBytes));
		//System.out.println("bytes = " + PrintBytes(licBytes));
		//System.out.println(licBytes.length);//768

		//ProcessSmartlet ps =new ProcessSmartlet();
		//ProcessSmartlet.APNLicenseLibrary li =ps.new APNLicenseLibrary("");

		//--02. Generate a KeyFactory (RSA)
		String str = null;
      	KeyFactory localKeyFactory = null;
      	try
      	{
			//str = "RSA/NONE/PKCS1Padding";
			//localKeyFactory = KeyFactory.getInstance("RSA", "BC");

			str = "RSA";
        	localKeyFactory = KeyFactory.getInstance("RSA");
		}
		catch (NoSuchAlgorithmException e)
		{
		  //e.printStackTrace();
		  System.out.println(e); 
		}
		/*
		catch (NoSuchProviderException e)
		{
		  e.printStackTrace();
		}
		*/
      	
      	
		//--03. Generate PublicKey
		String publicKey = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhSO2mh+ql9fA850zd4WiMprQfY4l+Rtvo+yVkxKGVGX8028uBB8/TFIv4gDZSGTp36DJNSQ+U27eXOXeB3mMRry66Nn/+TPo3q/+k2Vkk+kBiWsXBVv9FWN94PRnD2dsTlVOuqWTPyF11D8Pwbma5oLymTY4bSqJoAwNB1Fvhuw5a616HPUeP/heACrmmomXv+oyOYbgTfjxixkhOh5NCjGZmhk8tgITy+f7tpWzjr2EsG0MlUbhlm5u+iUzH+9DwdodK04F46QdjeBRcnePdTFYbZQZ6GBLveLp7yb4YxFAFq5XcK5knvFWjROaHWtHUzS2fnsr5yp+lfVEoIMgxwIDAQAB";
		byte[] publicKeyArrayOfByte = Base64Util.decode(publicKey);
		X509EncodedKeySpec localX509EncodedKeySpec = new X509EncodedKeySpec(publicKeyArrayOfByte);

		PublicKey localPublicKey = null;

      	try
      	{
			localPublicKey = localKeyFactory.generatePublic(localX509EncodedKeySpec);
		}
		catch (InvalidKeySpecException e)
		{
		  //e.printStackTrace();
		  System.out.println(e); 
		}

		//--04. Copy the encrypted license byte to another byte array by decrypting 256 byte at a time
		//byte[] copiedLicBytes = new byte[licBytes.length];
      	Arrays.fill(licBytes, (byte)0);
      	
      	int i = 0;
		int j = 245;//256
		int k = 0;
		int l=245;
		int n = 0;
		byte[] arrayOfByte2 = new byte[j];


		for (int m = 0; m < licBytes.length / j; m++)
      	{
			arrayOfByte2 = new byte[j];
			i++;
			if((i*l) > copiedLicBytes.length)
			{
				l=copiedLicBytes.length-n;
			}
			
			System.arraycopy(copiedLicBytes, m * j, arrayOfByte2, 0, l);
			byte[] arrayOfByte5 = null;

			try
			{
				arrayOfByte5 = encrypt(arrayOfByte2, localPublicKey, str);
			}
			catch (Exception e)
			{
			  //e.printStackTrace();
			  System.out.println(e); 
			}

			System.arraycopy(arrayOfByte5, 0, licBytes, k, arrayOfByte5.length);
			k += arrayOfByte5.length;
			n += arrayOfByte2.length;
		}

		System.out.println("GetEncryptedLicenseBytesFromXMLByte. licBytes.length:"+licBytes.length);//768

		//WriteToFile(decompressedArrayOfByte,"smartguideB.txt");
		
		//--06. convert the arraybyte
		//xml = new String(decompressedArrayOfByte);
		//System.out.println(xml);

		//WriteToFile(xml,"smartguideT.txt");

		return licBytes;
		/*
		*/

	}
	
	public static void WriteToFile(String fileContent) throws IOException
	{


		//fileContent = "Hello Learner !! Welcome to howtodoinjava.com.";

		FileWriter fileWriter = new FileWriter("D:\\Apps\\Java\\Decompile\\files\\samplefile2.lic");
		fileWriter.write(fileContent);
		fileWriter.close();
	}

	public static void WriteToFile(byte[] bytes) throws IOException
	{
		String path="D:\\Apps\\Java\\Decompile\\files\\samplefile2.lic";
		
		//FileOutputStream stream = new FileOutputStream(path);
		
		//stream.write(bytes);
		//WriteToFile(bytes,path);
	}

	public static void WriteToFile(byte[] bytes, String filename) 
	{
		String path="D:\\Apps\\Java\\Decompile\\files\\" +filename;
		try
		{
			FileOutputStream stream = new FileOutputStream(path);
			
			stream.write(bytes);
		}
		catch(IOException e)
		{
			System.out.println(e);
		}
	}

	public static void WriteToFile(String fileContent, String filename) 
	{
		String path="D:\\Apps\\Java\\Decompile\\files\\" +filename;
		try
		{
			FileWriter fileWriter = new FileWriter(path);
			fileWriter.write(fileContent);
			fileWriter.close();
		}
		catch(IOException e)
		{
			System.out.println(e);
		}
	}

	public static String PrintBytes(byte[] bytes)
	{
	    StringBuilder sb = new StringBuilder();
	    sb.append("[ ");
	    for (byte b : bytes) {
	        sb.append(String.format("0x%02X ", b));
	    }
	    sb.append("]");
	    return sb.toString();
	}

	public static String GetXMLFromEncryptedLicense_Backup()
    {
		String xml="";

		String licFileName = null;
		//licFileName = "C:\\temp\\smartguide.lic";
		//licFileName = "C:\\temp\\samplefile2.txt";
		//licFileName = "C:\\temp\\smartguide3.lic";
		licFileName = "D:\\Apps\\Java\\Decompile\\files\\smartguide.lic";
		//licFileName = "D:\\Apps\\Java\\Decompile\\files\\smartguide5.lic";
		//licFileName = "D:\\Apps\\Java\\Decompile\\files\\samplefile2.lic";

		Resolver resolver = new Resolver();

		byte[] licBytes= resolver.resolveBytes(licFileName, null);

		//System.out.println(Arrays.toString(licBytes));
		//System.out.println(new String(licBytes));
		//System.out.println("bytes = " + PrintBytes(licBytes));
		//System.out.println(licBytes.length);//768

		ProcessSmartlet ps =new ProcessSmartlet();
		ProcessSmartlet.APNLicenseLibrary li =ps.new APNLicenseLibrary("");

		String str = null;
      	KeyFactory localKeyFactory = null;
      	try
      	{

			//str = "RSA/NONE/PKCS1Padding";
			//localKeyFactory = KeyFactory.getInstance("RSA", "BC");

			str = "RSA";
        	localKeyFactory = KeyFactory.getInstance("RSA");
		}
		catch (NoSuchAlgorithmException e)
		{
		  //e.printStackTrace();
		  System.out.println(e); 
		}
		/*
		catch (NoSuchProviderException e)
		{
		  e.printStackTrace();
		}
		*/
		//String publicKey="";
		String publicKey = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhSO2mh+ql9fA850zd4WiMprQfY4l+Rtvo+yVkxKGVGX8028uBB8/TFIv4gDZSGTp36DJNSQ+U27eXOXeB3mMRry66Nn/+TPo3q/+k2Vkk+kBiWsXBVv9FWN94PRnD2dsTlVOuqWTPyF11D8Pwbma5oLymTY4bSqJoAwNB1Fvhuw5a616HPUeP/heACrmmomXv+oyOYbgTfjxixkhOh5NCjGZmhk8tgITy+f7tpWzjr2EsG0MlUbhlm5u+iUzH+9DwdodK04F46QdjeBRcnePdTFYbZQZ6GBLveLp7yb4YxFAFq5XcK5knvFWjROaHWtHUzS2fnsr5yp+lfVEoIMgxwIDAQAB";

		byte[] arrayOfByte1 = Base64Util.decode(publicKey);
		X509EncodedKeySpec localX509EncodedKeySpec = new X509EncodedKeySpec(arrayOfByte1);

		PublicKey localPublicKey = null;

      	try
      	{
			localPublicKey = localKeyFactory.generatePublic(localX509EncodedKeySpec);
		}
		catch (InvalidKeySpecException e)
		{
		  //e.printStackTrace();
		  System.out.println(e); 
		}

		int i = 0;
		int j = 256;
		int k = 0;
		byte[] arrayOfByte2 = new byte[j];
		byte[] arrayOfByte3 = new byte[licBytes.length];
      	Arrays.fill(arrayOfByte3, (byte)0);


		for (int m = 0; m < licBytes.length / j; m++)
      	{
			i++;
			System.arraycopy(licBytes, m * j, arrayOfByte2, 0, j);
			byte[] arrayOfByte5 = null;

			try
			{
				arrayOfByte5 = decrypt(arrayOfByte2, localPublicKey, str);
			}
			catch (Exception e)
			{
			  //e.printStackTrace();
			  System.out.println(e); 
			}

			System.arraycopy(arrayOfByte5, 0, arrayOfByte3, k, arrayOfByte5.length);
			k += arrayOfByte5.length;
		}

		byte[] arrayOfByte4 = deCompressData(arrayOfByte3);
		xml = new String(arrayOfByte4);
		//System.out.println(xml);
		return xml;
		/*
		*/

	}

	public static String GetXML()
	{
		String xml="";
		String licFileName = null;
		licFileName = "C:\\temp\\smartguide.txt";


		try(BufferedReader br = new BufferedReader(new FileReader(licFileName))) {
			StringBuilder sb = new StringBuilder();
			String line = br.readLine();

			while (line != null) {
				sb.append(line);
				sb.append(System.lineSeparator());
				line = br.readLine();
			}
			xml = sb.toString();
		}
		catch (Exception e)
		{
			//e.printStackTrace();
			System.out.println(e);
		}
		return xml;
	}
}