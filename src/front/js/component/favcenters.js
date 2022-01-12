import React , { useState, useContext, useEffect, Fragment } from "react";
import { BrowserRouter, Routes, Route, Link, NavLink} from "react-router-dom";
import { Context } from "../store/appContext.js";
import "../../styles/profile.scss";

const FavCenters = () => {
    const { store, actions } = useContext(Context);
    const user = {...store.currentUser.user};
    const [icon, setIcon] = useState(false);
    const heart = "far fa-heart unclicked active iconfavourite-profile";
    const heartFav = "fas fa-heart unclicked active iconfavourite-profile";


    const favourites = user.favourite_centers.map((favourite, index) => {
        return (
            <li key={index.toString()}>
                <NavLink className="link-navbar" to={`/profile/${favourite.id}`}>
                {favourite.name} 
                </NavLink >
                <button className="btnfavourite-profile"
                    onClick={event => {
                        event.preventDefault;
                        actions.deleteFavourites(favourite);
                    }}>
                    <i className="fas fa-heart unclicked active iconfavourite-profile" />
                    {/* <i 
                        className={icon ? heartFav : heart}
                        onClick={() => setIcon(prevState => !prevState)}
                    /> */}
                </button>
            </li>
        );
    });


    return (
        <ul className="fav-list-profile">{favourites}</ul>
    );
}

export default FavCenters;