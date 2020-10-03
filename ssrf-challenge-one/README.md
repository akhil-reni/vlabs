# SSRF Challenge One


The following challenge involves a bit of scripting to escalate an internal misconfiguration to full-read SSRF.

### Objectives

- Load https://wesecureapp.com/ to win this challenge.


### To spin up the vulnerable instance

```
docker-compose up -d
```

The app will not allow external hosts, so you need chain vulnerabilities to achieve a Full read SSRF.
```
http://localhost:5000/proxy?url=https://test.com
```
