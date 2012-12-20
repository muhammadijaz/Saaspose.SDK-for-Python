'''
Created on Dec 10, 2012

@author: assad
'''
from common import *
import json
from _pyio import open

class OcrExtractor(object):
    
    def extract_text(self,filename,folder=None,language=None):
        try:
            #build URI            
            if(filename == ""):
                raise "Filename not found."
            
            str_uri_request = Product.base_product_uri + "/ocr/" + filename + "/recognize?useDefaultDictionaries=true"
            
            if(folder != None):
                str_uri_request = str_uri_request + "&folder=" + folder
            
            if(language != None):
                str_uri_request = str_uri_request + "&language=" + language
                        
            
            signed_uri = Utils.sign(Utils(),str_uri_request)
            
            response_stream = Utils.process_command(Utils(),signed_uri, "GET", "JSON", "")                       
                        
            json_data = json.loads(response_stream)
            
            if (json_data['Code'] != 200):
                return False
            else:
                return json_data["Text"]
                    
        except:
            raise
    
    def extract_text_from_local_file(self,local_filename,folder=None,language=None):
        try:
            #build URI            
            if(local_filename == ""):
                raise "Filename not found."
            
            with open(local_filename , "rb") as file_obj:
                file_data = file_obj.read()
                file_obj.close()
                
                        
            
            str_uri_request = Product.base_product_uri + "/ocr/recognize?useDefaultDictionaries=true"
            
            if(folder != None):
                str_uri_request = str_uri_request + "&folder=" + folder
            
            if(language != None):
                str_uri_request = str_uri_request + "&language=" + language
                        
            
            signed_uri = Utils.sign(Utils(),str_uri_request)
            
            response_stream = Utils.process_command(Utils(),signed_uri, "POST", "JSON", file_data)                       
                        
            json_data = json.loads(response_stream)
            
            if (json_data['Code'] != 200):
                return False
            else:
                return json_data["Text"]
                    
        except:
            raise