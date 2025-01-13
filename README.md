<img width="1512" alt="image" src="https://github.com/user-attachments/assets/b1d58647-32bd-4ded-976e-b1b08ed4f19c"><div align="center">
<h1>E-invoice Processing Platform</h1>
</div>


E-invoice Processing Platform is a platform for processing electronic invoices. It has three main functions: generating, validating, and sending invoices.

# Architecture

This platform is composed of the following architecture:

- **React**: frontend framework
- **Django**: backend framework
- **MySQL**: Database

### Other Tools and Technologies Used

- **Material UI**: layout and styles
- **Ant Design**: layout and styles


# Prerequisites

Before deploying the platform, ensure you have the following installed:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Deployment

Clone code to local
 ```sh
    git clone https://github.com/unsw-cse-comp99-3900-24t1/capstone-project-9900h16acrazythursday.git
 ```

To deploy the platform using Docker, open 'Docker Desktop' at first


Then run follow command at project directory:

1. **Remove any existing containers, images, volumes, and networks**:
    ```sh
    docker-compose down --rmi all --volumes --remove-orphans
    ```

2. **Build the Docker images**:
    ```sh
    docker-compose build
    ```

3. **Start the containers**:
    ```sh
    docker-compose up -d
    ```

After these steps, the E-invoice Processing Platform should be up and running. Go to [localhost:3000](http://localhost:3000/) and you can see the platform.


## Possible problems and solutions
### These problems are almost unlikely to occur, this part is just in case

<strong>Problem 1: </strong> Encounter "react-script not found" when starting "frontend" container<br>
<strong>Solution:  </strong> Run "npm install" at "/frontend" directory by terminal

<strong>Problem 2: </strong> Encounter ESLint issues become of cache problem<br>
<strong>Solution:  </strong> Close the issues page, it will not affect usage.

<strong>Problem 3: </strong> Encounter backend or database can not boot successfully at docker container. <br>
<strong>Solution:  </strong> Click the stop button on the top right of software. Then run
    ```
    docker-compose build
    ```
    and
    ```
    docker-compose up -d
    ```
    command to rebuild the project, repeat until backend and database boot successfully.

<strong>Problem 4: </strong> Encounter "failed to solve: error from sender: lstat /yourpath/capstone-project-9900h16acrazythursday/media/uploadInvoices: permission denied" <br>
<strong>Solution:  </strong> Open the code in VS Code, and enter the commands below in the terminal.
    ```
    sudo chmod a+x /yourpath/capstone-project-9900h16acrazythursday/media/uploadInvoices
    ```
    and
    ```
    sudo chown -R $(whoami):$(whoami) /yourpath/capstone-project-9900h16acrazythursday/media/uploadInvoices
    ```

# Test
## Important
Please use the pdf to ubl function in the creation module before August 5, 2024, as the API used for the PDF part will expire on August 5, 2024. Sorry for the inconvenience caused.

## Test converting PDF/JSON to UBL file in creation part.
**1.** Please use the provided PDF/JSON examples in 'TestExamples' folder if you do not have a PDF/JSON invoice. Attention: PDF format is supported before August 5, 2024.

**2.** If you encounter red box prompting you to 'Please Enter Customer ID (ABN)', please enter this example '91888222000' if you do not have an ABN. 

**3.** If you encounter red box prompting you to 'Please Enter your account number for payment', please enter this example '1987367458871009' if you do not have the financial account. 

**4.** If you encounter red box prompting you to 'Please Enter your PaymentTerms', please enter this example 'within 3 days' if you do not have other terms. 

## Test validation.
Please use the provided UBL (XML) examples in 'TestExamples' folder if you do not have a UBL (XML).

