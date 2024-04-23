# cateye-next
Cateye NEXT: NEXT Generation Installer

## Operating environment

**Python (Version 9 to 12)**

## How to use

### Download cateye-next

1. First, access to [Here](https://github.com/Kamu-JP/cateye-next/releases)
2. Next, click 'cateye.py' to download

### Run cateye-next

#### Windows
```
python /path/to/cateye.py
```

#### macOS
```
python3 /path/to/cateye.py
```

### Follow the instructions

### Done

## for Developers

### How to create software that can be installed with Cateye-next?

1. Create JSON File to Server (Static is also Okay)
2. Edit JSON (like Example)

**Example**
```
{
    "name": "software name",
    "url": "https://example.com/path/to/file.tar.gz",
    "folder": "Install folder (example: /usr/local/bin )",
    "version": "major version of cateye-next (example: 10)",
    "files": [

        "filename.ex"
    
    ],
    "dependencies": [

        "https://example.com/path/to/other-package.json"
  
    ],
    "script": [

        "Write the necessary Python processing here."
      
    ]
  }
```
