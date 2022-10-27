# Getting Started

> Your introduction to working on this project

**Authors**: Hallie(ha1lie), _______________________

## Where to start?

Looking at this repository, it might feel a bit overwhelming. Don't fret, below is a simple step-by-step guide to getting up and running! Start with whatever operating system you have!

## Prerequisites

No matter what your operating system, make sure to install the below apps before getting started. Doing so will make this process as easy as possible for you

- Visual Studio Code
    - This will be your best friend, especially if you haven't already gotten yourself your favorite code editor. 
    - [Download Link](https://code.visualstudio.com/download)
- Github Desktop
    - While not required, this will improve your quality of life if you're not super familiar with git cli, or branches and the like
    - [Download Link](https://code.visualstudio.com/download)

## MacOS

If you're a Mac user, don't look any further, it's a pretty simple setup, and won't take long :)

### Steps

1. Install Docker
2. Clone this repository
3. Build and run

### 1 - Installing Docker

Docker is a containerization platform which allows you to run a lot of services(like with what we're building) quite easily. While it does much more, this is why we are utilizing it

1. Navigate to [the docker download page](https://docs.docker.com/engine/install/) and click the download for your applicable Mac. Make sure to choose Intel or Apple Silicon accordingly
2. Open the .DMG file that was downloaded. Then, like any other Mac app, drag it to the applications folder
3. Close the DMG, and then open the newly installed Docker app
4. When you launch it for the first time, Docker will ask you for your administrator password. This is normal, and safe. Docker is a trusted tool.
5. Docker will load, potentially open another authorization prompt, let it load
6. Eventually, Docker will settle down, and you should see a window with a green bar in the bottom left corner

**NOTE:** If you do not see this green bar, or it is another color, feel free to ask for some guidance and we can troubleshoot it together

**NOTE 2:** Docker *Compose* is bundled with the Docker Desktop app. You do not need to install another thing

**SIGNIFICANT NOTE:** You will need to keep Docker running while you are working on this project. Without it, running docker containers will fail

### 2 - Clone this repository

This step is easy! If you are comfortable using the git CLI, you may do so. If not, open up Github Desktop, and let's get started.

1. In the top left corner of GH Desktop, click the down arrow, then click "Add"
2. This will prompt you if you would like to Clone, add new, or add existing. Select "Clone Repository..."
3. In the popup that appears, click into the "URL" tab
4. Paste in the URL to this directory into the URL box, and select the path you would like GH Desktop to clone it to
5. Click clone! Done!

**Repository URL:**
`https://github.com/Women-in-Computing-at-RIT/WicHacker-Manager`

### 3 - Build and run

Finally! You have the code, and everything you need to run it! The next part is super easy!

1. Open a terminal window. If you have VSCode installed, you can open the repository folder in that app, go up to your menu bar -> Terminal -> New Terminal and a window will open at the bottom of VSCode. If not, open up the default Terminal app on your Mac
2. `cd` into the repository directory. If you opened the VSCode app, you will already be here
3. You need to build the docker image! We've provided a script to do this for you. Type the below command and hit enter. The first time you run it, this could take a while... be patient

`./rebuildDockerImages.sh`

4. You need to start the docker container! Type the below command

`docker-compose up`

5. It should be running! You can test this by visiting `localhost:3000` in your browser window, and you should be greeted with plaintext! If not, time to troubleshoot. Please share error messages if you would like help
6. When you're done, you'll want to stop the docker container so it stops using resources. You can either `ctrl+c` out of the process if you're still running it, or if it's been lost, you can run `docker-compose down` and it will stop itself! 

## Windows

PC User? We've got you covered! For simplicities sake, make sure you install Visual Studio Code and Github Desktop. Directions will not be written without these

### Steps 

1. Install all the things
2. Clone repository
3. Build and run

### 1 - Installing all the things

**IF YOU HAVE THESE THINGS INSTALLED ALREADY, DO NOT REINSTALL THEM. YOUR CURRENT INSTALLATION WILL WORK**

#### Git

Windows does not come with git. Download the exe from [git's official site](https://git-scm.com/download/win), and launch it. Please note:

- Adjusting your PATH Environment: Choose *Git from the command line and also 3rd party software*. This allows GH Desktop and VSCode to utilize it

Everything else should be able to be left to default.

#### WSL 

WSL, or Window's Subsystem for Linux(backwardly defined, oddly enough), is a way to run unix-y commands on Windows, which typically operates with Microsoft's own PowerShell. Docker, which our project heavily relies on, requires WSL to work. Therefore, we'll install it ahead of time to prevent it from causing any issues later

I personally do not feel comfortable giving out install advice for this. Please see [Microsoft's Official Installation Guide]() to get started. 

I installed Ubuntu, and did not have any issues at all. 

If you want to trust me, you can just run `wsl --install` in Command Prompt, so long as it is running as administrator(right click when you launch it)

#### Docker

Docker is a containerization platform which allows you to run a lot of services(like with what we're building) quite easily. While it does much more, this is why we are utilizing it

1. Navigate to [the docker download page](https://docs.docker.com/engine/install/) and click the `Docker Download for Windows` button
2. Once it's downloaded, run the .exe file, clicking to allow changes. Again, Docker is a trusted source
3. Click install, and wait for it to do it's thing. When it's done, it will notify you, and ask you to log out, and or restart. Go ahead and let it do that
4. When you log back in, docker will automatically launch, and will start spinning. Give it a moment as it starts up, and eventually, you will see a tutorial. You are welcome to skip it.
5. If you are successful, Docker's app should have a green bar in the bottom left corner. If not, it's time to troubleshoot. Make sure to include all screenshots and error messages applicable

### 2 - Clone repository

Feel free to follow the directions below, which utilize GH Desktop, or, if you're comfortable, you can clone it any other way you would like. Please note, using Github Desktop will likely make your life easier later.

1. In the top left corner of GH Desktop, click the down arrow, then click "Add"
2. This will prompt you if you would like to Clone, add new, or add existing. Select "Clone Repository..."
3. In the popup that appears, click into the "URL" tab
4. Paste in the URL to this directory into the URL box, and select the path you would like GH Desktop to clone it to
5. Click clone! Done!

**Repository URL:**
`https://github.com/Women-in-Computing-at-RIT/WicHacker-Manager`

### 3 - Build and run

Running programs on Windows devices is often a little bit different than other platforms due to Powershell, Microsoft's version of bash, or zsh, often used in unix systems. To eliminate some of these issues, we'll be utilizing the fact that installing git also install's git's copy of bash, allowing us to run scripts used for other platforms. 

Below are instructions for completing this using Visual Studio Code, since it is the platform I am most comfortable with. If you'd prefer, you're welcome to use another shell, but this will detail opening a bash shell as well

1. Open the project in VSCode
2. In the menu bar, go to "Terminal" -> "New Terminal" and you will see a Powershell terminal open at the bottom of your window
3. On the top bar of the terminal section, click on the down arrow next to the "+" symbol
4. Click on "Git Bash". You'll see new colors in the terminal window, a different prompt ("$"), and on the right side you will see powershell and bash listed. From here on out you'll want to make sure bash is selected.
5. Run the command `./rebuildDockerImages.sh`. This will create a docker image. The first time you run it this may take a while
6. Run `docker-compose up`. This will start the docker container. It may end with errors(this will be fixed eventually), but everything should be up and running. 

Yay! Let's test this progress. Go to `localhost:3000` in your browser window, and you should see "WiCHacks Landing Page" in your browser window. If so, success! If not, it's time to do some trouble shooting, make sure to share all applicable error messages. 

## Finally!

Nice! Now it's time to get to work! You're prepared to be absolute STEM ROYALTY!