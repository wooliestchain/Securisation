# Securisation
.
Kerberos is a network authentication protocol that provides strong authentication for client/server applications over a non-secure network. It was developed by MIT (Massachusetts Institute of Technology) in the 1980s to address the problem of authentication over insecure networks, such as the internet. Kerberos is widely used in enterprise networks to provide secure authentication for a wide range of applications and services.

The name "Kerberos" comes from Greek mythology, where it was a three-headed dog that guarded the entrance to Hades. Similarly, the Kerberos protocol guards access to network resources by providing strong authentication and encryption.

The Kerberos protocol works on the basis of a trusted third-party authentication service called the Kerberos Key Distribution Center (KDC). The KDC acts as a central authority that issues tickets to authenticated users and services. These tickets are then used to access network resources without further authentication.

Here is an overview of the main components and processes involved in the Kerberos protocol:

User authentication: When a user logs into a Kerberos-enabled system, they provide their username and password. This information is sent to the KDC for authentication.

Ticket granting: If the user's credentials are valid, the KDC issues a Ticket Granting Ticket (TGT) to the user. The TGT contains a session key that will be used to authenticate subsequent requests.

Service authentication: When the user wants to access a service, such as a file server or web application, they present their TGT to the KDC. The KDC issues a Service Ticket that contains the session key and other information necessary to access the requested service.

Service access: The user presents the Service Ticket to the service, which validates it and grants access to the requested resource.

The Kerberos protocol provides several security features, including:

1.Mutual authentication: Both the client and server authenticate each other, ensuring that the connection is secure and not vulnerable to man-in-the-middle attacks.
2.Confidentiality: The Kerberos protocol encrypts all data exchanged between the client and server, ensuring that it cannot be intercepted or read by unauthorized parties.
3.Ticket expiration: Kerberos tickets have a limited lifetime, which helps to reduce the risk of unauthorized access if a ticket is compromised.
4.Replay protection: Kerberos uses nonces to protect against replay attacks, where an attacker intercepts and replays a message to gain access to a resource.



Overall, Kerberos is a widely-used and trusted protocol for network authentication and security. By providing strong authentication and encryption, it helps to ensure that network resources are secure and accessible only to authorized users.



We'll use Pyhthon to make a simple authentification using kerberos .


Here is what we need to able to do so :

First we need to make sure Python is installed and up to date 

```bash
sudo apt update
```
```bash
sudo apt install python3 python3-pip
```


Now we need to add the dependecies we'll use in the project:
```bash
pip3 install flask flask-kerberos
```

Warning!!!!!
You may encoutner some issue here, so if it the case you'll have to install flask first and then flask-kerberos :
```bash
pip3 install flask
```
And then:
```bash
pip3 install flask flask-kerberos
```

So now we have to install the kerbros server , our simple app will use it for the AUTH.

Make sure everything is up to date:
```bash
sudo apt update
```

after this:
```bash
sudo apt install krb5-kdc krb5-admin-server
```

After the installation of our server , we have to make some configuration 

You will have to open the file krb5.conf , you can do so with this command

```bash
sudo nano /etc/krb5.conf
```
The configuration depends on your need is totaly up to you, but bellow you'll have an exemple:

```bash
[libdefaults]
  default_realm = EXAMPLE.COM
  dns_lookup_realm = false
  dns_lookup_kdc = false
  ticket_lifetime = 24h
  renew_lifetime = 7d
  forwardable = true

[realms]
  EXAMPLE.COM = {
    kdc = kerberos.example.com
    admin_server = kerberos.example.com
  }

[domain_realm]
  .example.com = EXAMPLE.COM
  example.com = EXAMPLE.COM
```

Default name is **EXAMPLE.COM** and default kdc server is **kerberos.example.com**





For the suite , we'll have to create an administration :

```bash
sudo kadmin.local -q "addprinc admin/admin"
```
The first **admin** is the name and the second is the password, you can do as you want and give it anither name

Then you will have to add the users :
```bash
sudo kadmin.local -q "addprinc user1"
sudo kadmin.local -q "addprinc user2"
```

You can verify that it has work with the following command 
```bash
sudo kadmin.local -q "listprincs"
```
The command below will display all the principals users created previously 


You will also will have to deploy an HTTP service key for your application with the following command:
```bash
sudo kadmin.local -q "addprinc -randkey HTTP/webapp.example.com"
```

We have created a key for the application on the HTTP server , we used **randkey** , but you can specify the algorithm you want to use for the generation of your key .

Next we'll stock this key in the file with the command:
```bash
sudo kadmin.local -q "ktadd -k /etc/krb5.keytab HTTP/webapp.example.com"
```

And for the final step of Kerbros , we'll ad the authorisation for the two users created previously :
```bash
sudo kadmin.local -q "addprinc -policy user_policy +allow_login_as user1"
sudo kadmin.local -q "addprinc -policy user_policy +allow_login_as user2"
```




#Since our kerberos configuration is done , we can take a look at Python .

This code uses the Flask-Kerberos extension to handle Kerberos authentication. 

The / and /admin routes are protected and have valid authentication to access. 

The /logout route allows the user to log out. 

The handle_auth_error and handle_forbidden_error functions are called when authentication fails or if the user does not have the necessary permissions to access a resource.

To run the code , you can run the commande :
```bash
python3 app.py
```

**app.py** refers to the name of your Python file 
This app will run on the port 5000 in local .


**THANKS FOR READING**









