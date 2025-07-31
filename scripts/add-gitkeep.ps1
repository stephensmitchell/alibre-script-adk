#Requires -Version 5.1

<#
.SYNOPSIS
    Adds .gitkeep files to empty directories in a repository.

.DESCRIPTION
    This script recursively scans a directory tree and adds .gitkeep files to any empty directories.
    The .gitkeep files help preserve empty directory structure in Git repositories.

.PARAMETER Path
    The root path to scan for empty directories. Defaults to current directory.

.PARAMETER Exclude
    Array of directory names to exclude from processing (e.g., '.git', 'node_modules').

.PARAMETER DryRun
    When specified, shows what would be done without actually creating files.

.PARAMETER Force
    When specified, overwrites existing .gitkeep files.

.EXAMPLE
    .\add-gitkeep.ps1
    Adds .gitkeep files to all empty directories in the current directory.

.EXAMPLE
    .\add-gitkeep.ps1 -Path "C:\MyProject" -DryRun
    Shows what .gitkeep files would be created in the specified path.

.EXAMPLE
    .\add-gitkeep.ps1 -Exclude @('.git', 'node_modules', 'bin', 'obj')
    Excludes common build and version control directories.
#>

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$Path = ".",
    
    [string[]]$Exclude = @('.git', '.vs', 'bin', 'obj', 'node_modules', '.vscode'),
    
    [switch]$DryRun,
    
    [switch]$Force
)

# Resolve the path to absolute
$RootPath = Resolve-Path -Path $Path -ErrorAction Stop
Write-Host "Scanning directory: $RootPath" -ForegroundColor Green

# Counter for tracking results
$EmptyDirsFound = 0
$GitkeepCreated = 0
$GitkeepSkipped = 0

# Function to check if directory is empty (excluding .gitkeep files)
function Test-DirectoryEmpty {
    param([string]$DirectoryPath)
    
    $items = Get-ChildItem -Path $DirectoryPath -Force | Where-Object { $_.Name -ne '.gitkeep' }
    return ($items.Count -eq 0)
}

# Function to generate .gitkeep content based on directory name
function Get-GitkeepContent {
    param([string]$DirectoryName)
    
    $directoryTitle = (Get-Culture).TextInfo.ToTitleCase($DirectoryName.ToLower())
    
    return @"
# $directoryTitle Directory

This directory is intended for $DirectoryName related files and components.

Please place your $DirectoryName files and related resources here.
"@
}

# Get all directories recursively, excluding specified directories
$allDirectories = Get-ChildItem -Path $RootPath -Directory -Recurse | Where-Object {
    $dirName = $_.Name
    $exclude = $false
    foreach ($excludePattern in $Exclude) {
        if ($dirName -like $excludePattern) {
            $exclude = $true
            break
        }
    }
    return -not $exclude
}

# Include the root directory if it's empty
$allDirectories = @(Get-Item -Path $RootPath) + $allDirectories

Write-Host "Found $($allDirectories.Count) directories to check" -ForegroundColor Cyan

foreach ($directory in $allDirectories) {
    if (Test-DirectoryEmpty -DirectoryPath $directory.FullName) {
        $EmptyDirsFound++
        $gitkeepPath = Join-Path -Path $directory.FullName -ChildPath '.gitkeep'
        $relativePath = $directory.FullName.Replace($RootPath, '.').Replace('\', '/')
        
        Write-Host "Empty directory found: $relativePath" -ForegroundColor Yellow
        
        # Check if .gitkeep already exists
        if (Test-Path -Path $gitkeepPath) {
            if ($Force) {
                if ($DryRun) {
                    Write-Host "  [DRY RUN] Would overwrite: $relativePath/.gitkeep" -ForegroundColor Magenta
                } else {
                    $content = Get-GitkeepContent -DirectoryName $directory.Name
                    Set-Content -Path $gitkeepPath -Value $content -Encoding UTF8
                    Write-Host "  Overwritten: $relativePath/.gitkeep" -ForegroundColor Green
                    $GitkeepCreated++
                }
            } else {
                Write-Host "  Skipped (already exists): $relativePath/.gitkeep" -ForegroundColor Gray
                $GitkeepSkipped++
            }
        } else {
            if ($DryRun) {
                Write-Host "  [DRY RUN] Would create: $relativePath/.gitkeep" -ForegroundColor Magenta
            } else {
                $content = Get-GitkeepContent -DirectoryName $directory.Name
                New-Item -Path $gitkeepPath -ItemType File -Value $content -Force | Out-Null
                Write-Host "  Created: $relativePath/.gitkeep" -ForegroundColor Green
                $GitkeepCreated++
            }
        }
    }
}

# Summary
Write-Host "`nSummary:" -ForegroundColor Cyan
Write-Host "  Empty directories found: $EmptyDirsFound" -ForegroundColor White
if ($DryRun) {
    Write-Host "  .gitkeep files that would be created: $EmptyDirsFound" -ForegroundColor Magenta
} else {
    Write-Host "  .gitkeep files created: $GitkeepCreated" -ForegroundColor Green
    Write-Host "  .gitkeep files skipped: $GitkeepSkipped" -ForegroundColor Gray
}

if ($DryRun) {
    Write-Host "`nRun without -DryRun to actually create the files." -ForegroundColor Yellow
}
