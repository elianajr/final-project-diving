import React , { useState, useContext, useEffect, Fragment } from "react";
import { useForm, useParams } from "react-hook-form";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Context } from "../store/appContext.js";
import "../../styles/profile.scss";

const FavButton = () => {
    const { store, actions } = useContext(Context);
    const { watch, register, formState: { errors }, handleSubmit } = useForm({mode:"all"});
    const user = {...store.currentUser.user};
    const [icon, setIcon] = useState(false);
    const heart = "far fa-heart unclicked active iconfavourite-profile";
    const heartFav = "fas fa-heart unclicked active iconfavourite-profile";
    const result = {...store.currentUser.result};
    const fav = user.favourite_spot;
    


	// const onSubmit = data => {
	// 	console.log(fav);
	// 	console.log('Este es el siguiente log', user.id)
	// 	actions.addFavCenter(fav, user.id);
	// };

    useEffect(()=>{
        console.log("hola", user);
    },[])

    return (
        // <form onSubmit={handleSubmit(onSubmit)}>
        <button className="btnfavourite-profile"
        // onClick={actions.addFavCenter()}
        // type="submit"
        >
            <i 
            className={icon ? heart : heartFav}
            onClick={() => setIcon(prevState => !prevState)}
            />
        </button>
        // </form>
    );
}

export default FavButton;