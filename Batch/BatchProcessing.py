import win32com.client
# from appscript import *
import os, sys
psApp = win32com.client.Dispatch("Photoshop.Application")

psApp.Open(r"C:\Users\37\Desktop\Demo.psd")

# file = 'ExportPSDUI.jsx'

filelist = sys.argv[1:]

jsCode = """
var g_StackScriptFolderPath = app.path + "/Presets/Scripts/" 
var runMergeToHDRFromScript = true; 
$.evalFile(g_StackScriptFolderPath + "Export PSDUI.jsx");

mergeToHDR.mergeFilesToHDR(%s, true);
""" % (repr(filelist),)

psApp.DoJavaScript(jsCode)