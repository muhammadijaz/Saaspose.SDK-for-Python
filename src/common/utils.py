'''
Created on Dec 6, 2012

@author: assad
'''
import pycurl
from urlparse import urlparse
import hashlib
import json
import hmac
import StringIO
import os.path
import re
from saasposeapp import SaasposeApp

class Utils:
    buf = StringIO.StringIO();
    buf_uploadFile   = StringIO
    
    @staticmethod
    def process_command(self,url,method="GET",header_type="XML",src=""):
        
        response_buf = StringIO.StringIO()        
        
        method = method.upper()
        header_type = header_type.upper()
        
        session = pycurl.Curl()
        session.setopt(pycurl.URL,url)
        
        if(method is "GET"):
            session.setopt(pycurl.HTTPGET,1)
        else:
            session.setopt(pycurl.POST,1)
            session.setopt(pycurl.POSTFIELDS,src)
            session.setopt(pycurl.CUSTOMREQUEST,method)
        
        session.setopt(pycurl.HEADER,False)
        session.setopt(pycurl.WRITEFUNCTION,response_buf.write)
        
        if (header_type == "XML"):
            session.setopt(session.HTTPHEADER, ['Accept: application/xml', 'Content-Type: application/xml']);
        else:
            session.setopt(session.HTTPHEADER, ["Content-Type: application/json"]);
        
        if(re.search("https",url)):
            session.setopt(pycurl.SSL_VERIFYPEER,False)
        
        session.perform()
        result = response_buf.getvalue()
        
        session.close()
        
        return result
        
    @staticmethod
    def upload_file_binary(self, url, localfile, header_type="XML"):
        header_type = header_type.upper();
        fp = open(localfile, 'rb');
#               
        c = pycurl.Curl();
        c.setopt(pycurl.URL, url);
        c.setopt(pycurl.VERBOSE, 1);
        c.setopt(pycurl.USERPWD, 'user:password');
        c.setopt(pycurl.PUT, 1);
#        c.setopt(pycurl.RETURNTRANSFER, 1)
        c.setopt(pycurl.HEADER, False);
                    
        if (header_type == "XML"):
            c.setopt(c.HTTPHEADER, ['Accept: application/xml', 'Content-Type: application/xml']);
        else:
            c.setopt(c.HTTPHEADER, ["Content-Type: application/json"]);
        
        c.setopt(pycurl.INFILE  , fp);
        c.setopt(pycurl.WRITEFUNCTION, self.buf_uploadFile.write);
        c.setopt(pycurl.INFILESIZE  , os.path.getsize(localfile));
        
        result =    c.perform();
        c.close();
        fp.close();
        return result;
              
    @staticmethod
    def sign(self,url_to_sign):
                
        url_to_sign = url_to_sign.replace(" ", "%20");
                
        url = urlparse(url_to_sign);
             
        if (url.query == ""):
            url_part_to_sign = url.scheme + "://" + url.netloc + url.path + "?appSID=" + SaasposeApp.app_sid
        else:
            url_part_to_sign = url.scheme + "://" + url.netloc + url.path + "?" + url.query + "&appSID=" + SaasposeApp.app_sid
 
        signature = hmac.new(SaasposeApp.app_key, url_part_to_sign, hashlib.sha1).digest().encode('base64')[:-1]
        signature = re.sub('[=_-]','',signature)
                
        if (url.query == ""):
            return url.scheme + "://" + url.netloc + url.path + "?appSID=" + SaasposeApp.app_sid + "&signature=" + signature
        else:
            return url.scheme + "://" + url.netloc + url.path + "?" + url.query + "&appSID=" + SaasposeApp.app_sid + "&signature=" + signature
        
    @staticmethod        
    def validate_output(self,result):
        str_result = str(result);
        
        validate = ["Unknown file format.", "Unable to read beyond the end of the stream", 
        "Index was out of range", "Cannot read that as a ZipFile", "Not a Microsoft PowerPoint 2007 presentation",
        "Index was outside the bounds of the array", "An attempt was made to move the position before the beginning of the stream"
        ];

        invalid = 0;
        for key in validate:
            if key == str_result:
                invalid = 1
                 
        if invalid == 1:
            return str_result;
        else:
            return ""
    
    @staticmethod
    def get_field_value(self,json_response, field_name):
        in_json = json.loads(json_response);
        return in_json.get(field_name);
    
    @staticmethod        
    def get_field_count(self,json_response, field_name):
        in_json = json.loads(json_response);
        return len(in_json);
    
    @staticmethod
    def save_file(self,input_data, filename):
        try:
            f=open(filename, 'w');
            f.write(input_data);
            f.close();
        except:
            return "error"
    
    @staticmethod
    def get_filename(self,filename):
        absolute_path = os.path.abspath(filename);
        base = os.path.basename(absolute_path)
        filename = os.path.splitext(base)[0]
        return filename
    
    @staticmethod
    def copy_stream(self,input_stream):
        return 