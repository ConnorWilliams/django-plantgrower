# Plant Grower
Django project and django-plantgrower app

## Uses
- Django
- Django Channels for websockets
- Django REST framework for API
- Python Celery for:
  - Periodic tasks such as monitoring and sending data to front end
  - Task Queue for monitoring tasks
- Redis for Channels and Celery backend
- RabbitMQ to send instructions to IoT devices

## Architecture Diagram
[Link to draw.io]()

## Deployment
All components have a Dockerfile and therefore is easily deployed with Kubernetes. You can deploy this locally on a Raspberry Pi, for example, for maximum privacy. However it is scalable so you can deploy in to a managed container engine and run there.

### Raspberry Pi
There are a couple of things to do before we deploy the application, I will not try and do a better job of explaining than [Alex Ellis](https://github.com/alexellis) who has already done it so well. My scripts are based on his.
1. [Provision a Raspberry Pi](https://github.com/ConnorWilliams/provision_raspberry_pi)
2. Install Docker on a Raspberry Pi
    ```bash
    curl -sSL https://get.docker.com | sh
    ```
3. Set Docker to auto-start
    ```bash
    sudo systemctl enable docker
    ```

4. Reboot the Pi, or start the Docker daemon with:
    ```bash
    sudo systemctl start docker
    ```

5. Enable Docker client
   
    The Docker client can only be used by root or members of the docker group. Add pi or your equivalent user to the docker group:
    ```bash
    sudo usermod -aG docker pi
    ```
6. Install Docker Compose
    
    Compose can also be run inside a container, from a small bash script wrapper. To install compose as a container run this command:
    ```bash
    sudo curl -L --fail https://github.com/docker/compose/releases/download/1.24.0/run.sh -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    ```

    ```bash
    curl -L https://github.com/docker/compose/releases/download/1.24.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    ```