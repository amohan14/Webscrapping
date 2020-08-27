# Webscrapping
- Install Anisible on local machine or virtual machine
    ###### Linux/MacOs
        $ sudo apt update
        $ sudo apt install software-properties-common
        $ sudo apt-add-repository --yes --update ppa:ansible/ansible
        $ sudo apt install ansible
    ###### CentOs
        $ sudo yum install python3-pip
        $ sudo pip install --upgrade pip
        $ sudo pip3 install ansible

- Ansible will connect to AWS using boto SDK. So we have to install boto and boto3 ackages on our local machine or VM

        $ sudo pip3 install boto boto3

- Go to AWS console and create an IAM User. Add it to a group each having AmazonEC2FullAccess permissions. 

- Copy the user's AWS Access Key ID and AWS Secret Access Key

- Return to Virtual Machine. Configure AWS with the user keys and set the default region as per requirement

        $ aws configure
        
- Also create an **.aws/credentials** file and copy the keys and default region to it so that ansible can access the keys accordingly

- Create a keypair and ensure the keypair.pem file is accessible to virtual machine. 

- Create an EC2 Instance(CentOs machine) using Ansible playbook and add host to group 'just_created' with variable foo=42

        - name: Create an EC2 instance
            hosts: local
            connection: local
            gather_facts: False
            tasks:
                - name: Launch instance
                 ec2:
                    key_name: ansible-lab
                    group: ansible-node
                    instance_type: t2.micro
                    image: ami-02354e95b39ca8dec
                    wait: true
                    region: us-east-1
                    # aws_access_key: "{{ lookup('env', 'AWS_ACCESS_KEY') }}"
                    # aws_secret_key: "{{ lookup('env', 'AWS_SECRET_KEY') }}"
                register: ec2
                - name: Print all ec2 variables
                debug: var=ec2
                - name: Get the Ip address
                debug: var=ec2.instances[0].public_dns_name

                 - name: add host to group 'just_created' with variable foo=42
                    add_host:
                    name: "{{ ec2.instances[0].public_dns_name }}"
                    groups: ec2_hosts
                    ansible_host: "{{ ec2.instances[0].public_dns_name }}"
                    ansible_ssh_user: ec2-user
                    ansible_ssh_private_key_file: /vagrant_data/ansible-lab.pem
    Replace the following values in the playbook:
    
        hosts: localhost
        key_name: name of the key-pair you will use to ssh to ec2 instance.
        group: security group of ec2 (ssh port should be open for the security group used)
        instance_type, image : as per the ec2 instance you want to create.
        region: as per the requirement.
    Make sure that the full path to .pem key file is profided to the "ansible_ssh_private_key_file" parameter

- Install packages onthe EC2 instance:
This step can be done manually after sshing to the EC2 instance or automatically through ansible playbook.
*First method:*
Execute the below commands based on the OS of EC2 instances for installing following packages:
**1. python**

    ###### Ubuntu
        $ sudo apt-get update && sudo apt-get upgrade -y
        $ sudo apt-get install python3.7

    ###### CentOs
        $ sudo yum install -y https://repo.ius.io/ius-release-el7.rpm
        $ sudo yum update -y
        $ sudo yum install -y python36u python36u-libs python36u-devel python36u-pip

    **2. pip**

    ###### CentOS-7 and higher
    Install pip in CentOS, using yum and python3 package manager:
    
        $ sudo yum install python3-pip
        $ sudo pip install --upgrade pip

    ###### Ubuntu
    Install pip in Ubuntu, using apt-get package manager:
    
        $ sudo apt-get update -y
        $ sudo apt-get install python3-pip
        $ sudo pip install --upgrade pip

    **3. git**

    ###### CentOs
        $ sudo yum install git

    ###### Ubuntu
        $ sudo apt-get install git

    **4. mariadb server**

    ###### CentOs
        $ sudo yum install mariadb-server

    For starting the mysql server.
    
        $ sudo systemctl start mariadb
        $ sudo systemctl status mariadb
        $ sudo echo -e "\n\nroot\nroot\n\n\nn\n\n " | mysql_secure_installation 2>/dev/null
    Note:
    -e        enable interpretation of the following backslash escapes
    2>/dev/null will filter out the errors so that they will not be output to your console. In more detail: 2 represents the error descriptor, which is where errors are written to. ... /dev/null is the standard Linux device where you send output that you want ignored.   
    
    ###### Ubuntu
    
        $ sudo apt update
        $ sudo apt install mariadb-server
        $ sudo echo -e "\n\nroot\nroot\n\n\nn\n\n " | mysql_secure_installation 2>/dev/null

    **4. BeautifulSoup4**
    ###### CentOs
        $ sudo pip3 install bs4
    
    ##### Ubuntu
        $ sudo apt-get update -y
        $ sudo apt-get install -y python3-bs4
        $ sudo apt-get install -y python-beautifulsoup
    
    **5. Requests**
    ###### CentOs
        $ sudo pip3 install requests
    
    ###### Ubuntu
        $ sudo apt-get update -y
        $ sudo apt-get install -y python3-requests
    
    *Second Method:*
    **Using Ansible Tasks to install all above packages:**
    
        name: Install packages into ec2 hosts
        hosts: ec2_hosts
        become: yes
        tasks:
            - yum: pkg=python3 state=latest
            - yum: pkg=python3-pip state=latest
            - yum: pkg=git state=installed
            - yum: pkg=mariadb-server state=installed
            - shell: sudo systemctl start mariadb
            - shell: echo -e "\n\nroot\nroot\n\n\nn\n\n " | mysql_secure_installation 2>/dev/null
            - shell: sudo pip3 install requests bs4
            
- After the packages are installed successfully, clone the git repository in which the webscrapper python script is present to the EC2 instance home directory.
    
        $ git clone https://github.com/amohan14/Webscrapping.git

- Run the Webscrapper python file and it shuld successfully outputs a .csv file containing all the reviews and their corresponding details.

        $ python3 Webscrapping/yelp_reviews_scrapping.py

To automate the above 2 points, we can add task to ansible playbook as follows:

    tasks:
        - shell: git clone https://github.com/amohan14/Webscrapping.git        
        - shell: python3 Webscrapping/yelp_reviews_scrapping.py

You can find the complete Ansible Playbook 
