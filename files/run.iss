; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Feni Med Store"
#define MyAppVersion "4.0"
#define MyAppPublisher "Md. Mydul Islam Anik"
#define MyAppURL "https://www.facebook.com/anik.i.khan/"
#define MyAppExeName "login.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{08D9E7A2-38CD-4702-9717-29D94673ACF4}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DisableProgramGroupPage=yes
OutputBaseFilename=FeniStoreSetup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "G:\Projects\TKinter_Python\Pharmacy_Management_System\login.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "G:\Projects\TKinter_Python\Pharmacy_Management_System\admin.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "G:\Projects\TKinter_Python\Pharmacy_Management_System\home.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "G:\Projects\TKinter_Python\Pharmacy_Management_System\icon.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "G:\Projects\TKinter_Python\Pharmacy_Management_System\login.spec"; DestDir: "{app}"; Flags: ignoreversion
Source: "G:\Projects\TKinter_Python\Pharmacy_Management_System\plus.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "G:\Projects\TKinter_Python\Pharmacy_Management_System\registerAdmin.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "G:\Projects\TKinter_Python\Pharmacy_Management_System\registerAdmin.spec"; DestDir: "{app}"; Flags: ignoreversion
Source: "G:\Projects\TKinter_Python\Pharmacy_Management_System\registerUser.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "G:\Projects\TKinter_Python\Pharmacy_Management_System\registerUser.spec"; DestDir: "{app}"; Flags: ignoreversion
Source: "G:\Projects\TKinter_Python\Pharmacy_Management_System\build\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{commonprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

