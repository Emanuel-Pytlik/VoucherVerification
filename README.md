# VoucherVerification
This repository contains all files related to the project to easily verify vouchers.


## Running the server

Make sure you have recent versions of `node` and `npm` installed (definitely at least version 12 of Node).
Installation instructions for most operating systems are available [on the Node.js website](https://nodejs.org/en/download).
You can check your `node` and `npm` versions using the following commands:

```bash
node --version
npm --version
```

Node.js is a tool that enables you to run JavaScript code outside of the web browser; it's a full-featured language runtime just like the `python3` or `java` command, and you can build desktop software using Node.js.
In this case, we'll use it to run a simple Web server that serves files from the project directory.
Although the code in `server.js` is written in JavaScript just like the JavaScript code within the `public/` directory, the code runs very differently.
In the &ldquo;real world&rdquo;, as a Web developer, you would run `server.js` on some computer you control in the cloud (say, an Amazon AWS server).
When people visit your website, they download HTML, CSS, and JavaScript code from your server, and that frontend code runs on their own computer.

Since you're developing this project locally, all of the code will live and run on your own computer.
Code in `server.js`, however, runs within the Node.js runtime, and the downloaded code in the `public/` directory will run within your web browser, which communicates with the web browser much as it would communicate with a real remote server when you typically brows the Internet.

### Installing the server dependencies

This repository contains a `package.json` file, which is the standard way to tell Node.js some information about the program, including what libraries are needed to run the server code.
The server software requires an external library called [Express](https://expressjs.com/), which makes it easy to develop Web servers.

Run the `install` command in `npm`, Node's default package manager:

```bash
npm install
```

This will read `package.json`, then look to the [NPM package repository](https://www.npmjs.com/) to grab the appropriate dependencies.

### Run the server

Run the server script on your development computer:

```bash
node server.js
```

This will start a long-running process (though you should be able to stop it with `Ctrl+C` or by closing your terminal window).
The server binds to `localhost:8000`, by default, meaning you should be able to access the web server by visiting [http://localhost:8000](http://localhost:8000) in your Web browser.

If you need to change the port or host, the server code will also accept a port number or host from the environment, which looks like this on macOS or Linux:

```
HOST=0.0.0.0 PORT=3000 node server.js
```

This is handy if you already have a process running on port 8000 or if you need to bind to a more public network interface (typically useful **if you want to connect to the server from other devices on your network**, like a mobile phone).


## Make it your own!

Here's how this repository is laid out.

Edit the **HTML files** and the **CSS stylesheet** to make them your own! 

Edit **server.js** if you want to add new pages, change how pages route to one another, if you've renamed your HTML files, etc. 

```
starter-code
│   README.md            // You are here!
│   server.js            // our Node server that responds to browser requests
│   package.json         // tells Node how to install the dependencies our server needs
│
└───public               // this where all of our static content is stored
   │   index.html        // The initial view for our web site
   │   a.html            // these are other pages our website links to. You can add more, but 		
   │   b.html            //   you might want to update server.js to give them prettier URLs.
   │   c.html
   │
   └───css
   │  	│   styles.css   // our CSS stylesheet!
   │   
   └───images            //images used by our website are stored here
   	│   bunny.jpg 	
   	└───...
```

Alternatively: Delete everything and start over if you want to learn how to set this up on your own, or in your own way!
Here's some documentation that might be relevant:

- https://expressjs.com/en/starter/hello-world.html
- https://expressjs.com/en/4x/api.html#express
