const PORT = 3001;
const [PROTOCOL, HOST] = process.env.GITPOD_WORKSPACE_URL.split("://");
import jwt_decode from "jwt-decode";

const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			message: null,
			users:[],
			user:{},
			baseUrl: `${PROTOCOL}://${PORT}-${HOST}/api/`,
			currentUser: {},
			token: {},
			position: {
				latitude: null,
				longitude: null
			},
			weather: {},
			nextDaysWeather: {},
			hotspots: []
		},

		actions: {
			// Use getActions to call a function within a fuctio
			getMessage: () => {
				// fetching data from the backend
				fetch(process.env.BACKEND_URL + "/api/hello")
					.then(resp => resp.json())
					.then(data => setStore({ message: data.message }))
					.catch(error => console.log("Error loading message from backend", error));
			},
			getUsers:()=>{
				fetch(getStore().baseUrl.concat('account'))
	        .then(function(response) {
		          if (!response.ok) {
	              throw Error(response.statusText);
	        }
    // Read the response as json.
	              return response.json();
	        })
	            .then(function(responseAsJson) {
					setStore({ users: responseAsJson });
	                console.log(responseAsJson);
	        })
                .catch(function(error) {
	             console.log('Looks like there was a problem: \n', error);
                 });
			},
			login: async (data) => {
				const tokenDecode = token => {
					let decoded = jwt_decode(token);
					return decoded;
				};
				const opts = {
					method: 'POST',
					headers: new Headers({
						'Content-Type': 'application/json'
					}),
					body: JSON.stringify(data)
				};

				try{
					const resp = await fetch(getStore().baseUrl.concat("login"), opts)
					if (resp.status !== 200) {
						alert("There has been some error");
						return false;
					}

					const data = await resp.json();
					console.log("this came from the backend", data);
					localStorage.setItem("token", data.token);
					const tokenDecoded = tokenDecode(responseAsJson);
					console.log(tokenDecoded)
					setStore({ token : data.token });
					return true;
				}
				catch(error){
					console.error("There was an error!!", error);
					}

			},
			getUser:(id)=>{
				fetch(getStore().baseUrl.concat('account/',id))
	        .then(function(response) {
		          if (!response.ok) {
	              throw Error(response.statusText);
	        }
    // Read the response as json.
	              return response.json();
	        })
	        .then(function(responseAsJson) {
				if (id){
					setStore({ user: responseAsJson });
	                console.log(responseAsJson);
				}		
	        })
            .catch(function(error) {
	             console.log('Looks like there was a problem: \n', error);
                 });
			},

		    register: async data => {
				const opt = {
					method: 'POST',
					headers: new Headers({
						'Content-Type': 'application/json'
					}),
					body: JSON.stringify(data)
				};

				try{
					const resp = await fetch(getStore().baseUrl.concat("account"), opt)
					if (resp.status !== 201) {
						alert("There has been some error");
						return false;
					}

					const data = await resp.json();

					localStorage.setItem("token", data.token);
					setStore({ token : data.token });

					localStorage.setItem("currentUser", JSON.stringify(data.account));
					setStore({ currentUser : data.account});

					return true;
				}
				catch(error){
					console.error("There was an error!!", error);
					}


			},	
			setPosition: (coords) => {
				setStore({position: {
					latitude: coords.latitude,
					longitude: coords.longitude
				}})
			},

			getOnloadWeatherData: () => {
				console.log(process.env.FORECAST_API_KEY)
				console.log('position', getStore().position);
				fetch(`${process.env.FORECAST_BASE_URL}lat=${getStore().position.latitude}&lon=${getStore().position.longitude}&appid=${process.env.FORECAST_API_KEY}&units=metric`)
					.then(resp =>{
						if(resp.ok) {
							return resp.json();
						}
						
						throw new Error("Fail loading weather");
					})
					.then(data =>{
						setStore({ weather: {
							city: data.name,
							weatherMain: data.main,
							weatherCoord: data.coord,
							weatherSys: data.sys,
							weatherWeather: data.weather[0],
							weatherWind: data.wind,
						}});					
					})
					.catch(error => {
						console.log(error.message);
					});
			},
			getThreeDaysWeatherData: ()=>{
				fetch(`${process.env.FORECAST_THREE_DAYS}lat=${getStore().position.latitude}&lon=${getStore().position.longitude}&exclude=minutely,hourly&appid=${process.env.FORECAST_API_KEY}&units=metric`)
				.then(resp => resp.json())
				.then(data =>{
					console.log("THREE DAYS AFTER",data)
					setStore({nextDaysWeather: {
						weatherToday: data.daily[0],
						weatherTomorrow: data.daily[1],
						weatherNextDay: data.daily[2],
						weatherNextNextDay: data.daily[3]
					}})													
				})
				.catch(error => {
					console.log(error.message);
				});
			},
			getWeatherData:(city,country,APYKEY)=>{
			 	fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city},${country}&appid=${process.env.FORECAST_API_KEY}&units=metric`)
			 		.then(resp => resp.json())
			 		.then(data =>{
			 			setStore({ weather: {
							city: data.name,
							weatherMain: data.main,
							weatherCoord: data.coord,
							weatherSys: data.sys,
							weatherWeather: data.weather[0],
							weatherWind: data.wind,
						}});						
			 		})
			 		.catch(error => {
			 			console.log(error.message);
			 		});
			},
			getAllHotspots:()=>{
				fetch(getStore().baseUrl.concat('hotspots'))
					.then(resp => resp.json())
					.then(data => {
						setStore({hotspots:[...data]})
					})

					.catch(error => {
						console.log(error.message);
					});
			},

			searchHotspot:(data)=>{
				var myHeaders = new Headers();
				myHeaders.append("Content-Type", "application/json");

				var raw = JSON.stringify({'name':data});

				var requestOptions = {
				method: 'POST',
				headers: myHeaders,
				body: raw,
				redirect: 'follow'
				};

				fetch(getStore().baseUrl.concat('search'), requestOptions)
				.then(response => response.json())
				.then(data => {
					setStore({hotspots:[...data]})
					console.log(data)
				})
				.catch(error => console.log('error', error));
			},

			addNewHotspot:(data,image)=>{
				var myHeaders = new Headers();
				myHeaders.append("Content-Type", "application/json");

				var raw = JSON.stringify(data);

				var requestOptions = {
				method: 'POST',
				headers: myHeaders,
				body: raw,
				redirect: 'follow'
				};

				const uploadimagehotspot =(id)  => {
					if (image!=''){
						let body = new FormData();
					body.append('media', image);
					const options = {
						body,
						method: "POST"
					};
					fetch(getStore().baseUrl.concat('hotspotphoto/',id),options)
					.then(resp => resp.json())
					.then(data => console.log("Success!!!!", data))
					.catch(error => console.error("ERRORRRRRR!!!", error))

					}
					
				};

				fetch(getStore().baseUrl.concat('hotspots'), requestOptions)
				.then(response => response.json())
				.then(result => uploadimagehotspot(result.id))
				.catch(error => console.log('error', error));
			},
			verifylogin:()=>{
				const token=localStorage.getItem('token')
				if (token) {
					return true
				} else{
					return false
				}
			}
			
		}

	};

}


export default getState;
