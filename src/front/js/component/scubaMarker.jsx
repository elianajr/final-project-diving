import React, { useEffect, useContext, useState } from "react";
import {Marker, Popup} from 'react-leaflet'
import { Context } from "../store/appContext";
import L from 'leaflet';
import { useParams } from "react-router-dom";

export const ScubaMarker = () => {
    const { store, actions } = useContext(Context);
    const [detailElements, setDetailElement] = useState(null);

    let params = useParams();

    useEffect(()=>{
        actions.getAllHotspots(params.id);
        
    },[])

    const iconOrange = new L.icon({
        iconUrl:"https://i.ibb.co/09zZ5Td/icon-orange.png",
        iconAnchor: null,
        shadowUrl: null,
        ShadowSize:null,
        ShadowAnchor:null,
        iconSize:(45,45),
    })

    useEffect(
		() => { 
			setDetailElement(
				store.hotspots.map((index, info) => {
                    if(index.sport_id == 1){
                        return (
                            <div key={index.id}>
                                <Marker position ={{lat:index.latitude, lng:index.longitude}} element={info}  icon={iconOrange} >
                                    <Popup>{index.name}<br/><img src={index.photo} alt="" width="200" height="100" /></Popup>
                                </Marker>
                            </div>
					);
                    }
				})
			);
		},
		[store.hotspots]
	);
    return (
        <div>
            {detailElements}
        </div>
    );
}