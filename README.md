
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

Python script enables user to add/update/delete Datadog tags (user-defined tag) of multiple hosts at once

### Built With

* [Python](https://www.python.org/)

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* [python3](https://www.python.org/downloads/)
    ```shell
    $ python --version
    $ Python 3.9.2
    ```

### Installation

1. Install dependencies
   
   ```shell
   $ pip install requests
   ```

2. Create your own API KEY and APP KEY at [Datadog API and Application Keys](https://docs.datadoghq.com/account_management/api-app-keys/)
3. Clone the repo
   ```shell
   $ git clone https://github.com/pd-khanh/datadog-tag-api.git
   ```
4. Rename `config.json.tmpl` to `config.json`
5. Enter your API KEY and APP KEY in `config.json`
    ```json
    {
      "production" : {
          "account" : "optional:your_email_in_production_datadog",
          "apiKey" : "ENTER YOUR API KEY",
          "appKey" : "ENTER YOUR APP KEY"
      },
      "testing" : {
          "account" : "optional:your_email_in_testing_datadog",
          "apiKey" : "ENTER YOUR API KEY",
          "appKey" : "ENTER YOUR APP KEY"
    }
    ```

## Usage

```shell
$ python datadog-tag-api.py -h

Usage: py datadog-tag-api.py [--prod]

Options:
        --prod          Run script in Production mode
```

## Example

```diff
$ python datadog-tag-api.py

Datadog Tag API - khanhpham1091@gmail.com (Test)

List of actions
        1: Get tags
        2: Get host tags
        3: Add tags to hosts
        4: Update host tags
        5: Remove host tags

+ Your choice is [1-5]: 3
Select Hosts (filterbytag|regex)
 example: host:azurevm,zone:apac|^azvm.*[0-9]$
 example: host:azurevm
+ Enter your hosts (Leave empty to select ALL): host:aws
Tags: env:development
Are you sure you want to perform this action ?
Performing the operation "Add tags to hosts" on hosts (total: 2)
        aws-free-vm1
        aws-free-vm2
with tags ['env:development']
+ [Y] Yes   [N] No   (default is "N"): Y
Creating tags for host:aws-free-vm1 ...
success
{
    "host": "aws-free-vm1",
    "tags": [
        "env:development"
    ]
}
Creating tags for host:aws-free-vm2 ...
success
{
    "host": "aws-free-vm2",
    "tags": [
        "env:development"
    ]
}
---
Start over ?
+ [Y] Yes   [N] No   (default is "N"): N
Bye
```
<!-- CONTACT -->
## Contact
khanhpham1091@gmail.com