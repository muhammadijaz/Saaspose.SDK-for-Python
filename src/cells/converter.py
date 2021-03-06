'''
Created on Dec 13, 2012

@author: assad
'''

from common import *
import json

class CellsConverter(object):
    
    filename= ""
    saveformat = ""
    worksheet_name = ""
    
    def __init__(self,filename,worksheet_name=""):
        
        self.filename = filename
        self.saveformat = "xls"
        self.worksheet_name = worksheet_name
    
    def convert(self,saveformat=""):
        try:
            
            if(self.filename == ""):
                raise Exception("No filename specified.")
                        
            self.saveformat = saveformat
            #build URI
            str_uri_request = Product.base_product_uri +'/cells/' + self.filename + '?format=' + self.saveformat
            signed_uri = Utils.sign(Utils(),str_uri_request)
                        
            response_stream = Utils.process_command(Utils(),signed_uri, "GET", "", "")            
            
            v_output = Utils.validate_output(self,response_stream)
            
            if(v_output == ""):                
                Utils.save_file(self,response_stream, SaasposeApp.output_location + Utils.get_filename(self,self.filename) + "." + self.saveformat )
                return True
            else:
                return v_output
        except:
                raise