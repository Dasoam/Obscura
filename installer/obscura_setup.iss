; Obscura Installer Script for Inno Setup
; This Source Code Form is subject to the terms of the Mozilla Public
; License, v. 2.0. If a copy of the MPL was not distributed with this
; file, You can obtain one at https://mozilla.org/MPL/2.0/
;
; Copyright (c) 2025 Obscura Contributors

#define MyAppName "Obscura"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Obscura Contributors"
#define MyAppURL "https://github.com/Dasoam/Obscura"
#define MyAppExeName "Obscura.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
AppId={{A3D2F8E1-7B4C-4E9A-B5D6-1F8C2A0E3B74}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/issues
AppUpdatesURL={#MyAppURL}/releases

; ===== APPLICATION DESCRIPTION =====
; This appears in Windows "Apps & Features" and installer
AppComments=Privacy-First Research Browser - Zero telemetry, zero tracking, zero data collection. A local-first, privacy-by-architecture research browser that runs entirely on your machine.
AppContact=https://github.com/Dasoam/Obscura/issues

; ===== INSTALLATION SETTINGS =====
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
; License file (will show before installation)
LicenseFile=LICENSE.txt
; Info shown BEFORE installation begins
InfoBeforeFile=README_INSTALLER.txt
; Output settings
OutputDir=..\dist\installer
OutputBaseFilename=Obscura_Setup_{#MyAppVersion}

; ===== COMPRESSION (Maximum) =====
Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes
LZMADictionarySize=65536

; ===== VISUAL SETTINGS =====
SetupIconFile=..\obscura.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName} - Privacy Research Browser
WizardStyle=modern
WizardResizable=no

; ===== PRIVILEGES =====
; User-level install by default (no admin required)
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; ===== SYSTEM REQUIREMENTS =====
MinVersion=10.0
; 64-bit only
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; ===== VERSION INFO FOR EXE =====
VersionInfoVersion=1.0.0.0
VersionInfoCompany=Obscura Contributors
VersionInfoDescription=Obscura - Privacy-First Research Browser Setup
VersionInfoCopyright=Copyright (c) 2025 Obscura Contributors
VersionInfoProductName=Obscura
VersionInfoProductVersion=1.0.0

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Messages]
; Custom welcome message
WelcomeLabel1=Welcome to [name] Setup
WelcomeLabel2=This will install [name/ver] on your computer.%n%n[name] is a Privacy-First Research Browser that runs entirely on your machine with ZERO telemetry, ZERO tracking, and ZERO data collection.%n%nIt is recommended that you close all other applications before continuing.

; Custom finish message
FinishedLabel=Setup has finished installing [name] on your computer.%n%nYour privacy is protected. No data has been or will be collected.%n%nThe application may be launched by selecting the installed icons.

[Types]
Name: "full"; Description: "Full installation"
Name: "compact"; Description: "Compact installation"

[Components]
Name: "main"; Description: "Obscura Application"; Types: full compact; Flags: fixed
Name: "shortcuts"; Description: "Create shortcuts"; Types: full

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Components: shortcuts
Name: "startmenuicon"; Description: "Create Start Menu shortcut"; GroupDescription: "{cm:AdditionalIcons}"; Components: shortcuts; Flags: unchecked

[Files]
; Main executable
Source: "..\dist\Obscura.exe"; DestDir: "{app}"; Flags: ignoreversion; Components: main
; Include logs folder structure (empty folder for app to use)
Source: "..\dist\logs\*"; DestDir: "{app}\logs"; Flags: ignoreversion recursesubdirs createallsubdirs skipifsourcedoesntexist; Components: main

[Icons]
; Start Menu
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Comment: "Privacy-First Research Browser - Zero tracking, zero telemetry"; Components: shortcuts; Tasks: startmenuicon
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"; Comment: "Uninstall Obscura"; Components: shortcuts; Tasks: startmenuicon
; Desktop
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Comment: "Privacy-First Research Browser - Zero tracking, zero telemetry"; Tasks: desktopicon

[Run]
; Option to launch app after install
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up logs folder on uninstall (user data stays private - deleted completely)
Type: filesandordirs; Name: "{app}\logs"
Type: dirifempty; Name: "{app}"

[Registry]
; Add to Windows "Apps & Features" with full description
Root: HKCU; Subkey: "Software\{#MyAppName}"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\{#MyAppName}"; ValueType: string; ValueName: "Version"; ValueData: "{#MyAppVersion}"
Root: HKCU; Subkey: "Software\{#MyAppName}"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"

[Code]
// ===== CUSTOM PASCAL CODE =====

function InitializeSetup(): Boolean;
begin
  Result := True;
  // Could add custom checks here (e.g., check for running instances)
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Create logs directory if it doesn't exist
    CreateDir(ExpandConstant('{app}\logs'));
  end;
end;

// Show a privacy notice after installation
procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = wpFinished then
  begin
    // The finish page already shows our custom message
  end;
end;

function InitializeUninstall(): Boolean;
begin
  Result := True;
  // Optionally show a message about data being deleted
  // All data stays local and is removed with uninstall
end;
