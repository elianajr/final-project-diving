import React from "react";
import {
	BrowserRouter,
	Routes,
	Route
  } from "react-router-dom";


import { Home } from "./pages/home";
import injectContext from "./store/appContext";
import ChatForm from "./component/ChatForm.jsx";
import News from "./pages/News.jsx";

//create your first component
const Layout = () => {
	//the basename is used when your project is published in a subdirectory and not in the root of the domain
	// you can set the basename on the .env file located at the root of this project, E.g: BASENAME=/react-hello-webapp/
	const basename = process.env.BASENAME || "";

	return (
		<BrowserRouter>
			<Routes>
				<Route path="/" element={<Home />} />
				<Route path="/chat" element={<ChatForm />} />
				<Route path="/news" element={<News />} />
			</Routes>
		</BrowserRouter>
	);
};

export default injectContext(Layout);

