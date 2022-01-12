import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { Context } from "../store/appContext";
import { Navbar } from "../component/navbar";
import { Footer } from "../component/footer";
import Card from "react-bootstrap/Card";

import { SearchBar } from "../component/searchBar.jsx";

import imgnewshome from "../../img/imgnewshome.png";
import img2newshome from "../../img/imgnewshome2.png";
import img3newshome from "../../img/imgnewshome3.png";
import img4newshome from "../../img/imgnewshome4.png";
import img5newshome from "../../img/imgnewshome5.png";

import "../../styles/home.scss";

const Home = () => {
  const { store, actions } = useContext(Context);

  const kitesurf = (
    <img src="https://i.ibb.co/ssMzJnP/mdi-kitesurfing.png" alt="surf" />
  );
  const snorkel = (
    <img src="https://i.ibb.co/JBVt1Tt/mdi-diving-snorkel.png" alt="snorkel" />
  );
  const surf = (
    <img src="https://i.ibb.co/GVKWPVT/map-surfing.png" alt="kitesurf" />
  );
  const diving = (
    <img src="https://i.ibb.co/pfCWKG5/mdi-diving-helmet.png" alt="diving" />
  );

  return (
    <div className="home">
      <Navbar />

      <div className="home-topbody">
        <img
          className="home-topbody_img"
          src="https://i.ibb.co/jRsbvtf/whale.png"
          alt="humpback whale"
        />
        <div className="home-topbody__sports">
          <Link to="/surf">
            <button className="home-topbody__sports__buttons">
              {surf}SURF
            </button>
          </Link>
          <Link to="/snorkel">
            <button className="home-topbody__sports__buttons">
              {snorkel}SNORKEL
            </button>
          </Link>
          <Link to="/kitesurf">
            <button className="home-topbody__sports__buttons">
              {kitesurf}KITESURF
            </button>
          </Link>
          <Link to="/diving">
            <button className="home-topbody__sports__buttons">
              {diving}DIVING
            </button>
          </Link>
        </div>
      </div>

      <div className="home-bottonbody">
        <div className="home-bottonbody__services">
          <div className="home-bottonbody__services__forecast">
            <div className="home-bottonbody__services_button__left">
              <Link to="/forecast">
                <button className="buttonWTD_style">Forecast</button>
              </Link>
            </div>
            <div className="home-bottonbody__service_p">
              <p>
                Check-out weather conditions wherever you go and ensure the best
                contiditions for your activities.{" "}
              </p>
            </div>
          </div>
          <div className="home-bottonbody__services__hotSpot">
            <div className="home-bottonbody__service_p">
              <p>
                Find the best spots closest to you, or check nice places you
                want to discover on your adventure
              </p>
            </div>
            <div className="home-bottonbody__services_button__right">
              <Link to="/hotspot">
                <button className="buttonWTD_style">HotSpot</button>
              </Link>
            </div>
          </div>
          <div className="home-bottonbody__services__hotSpot">
            <div className="home-bottonbody__services_button__left">
              <Link to="/hotspot">
                <button className="buttonWTD_style">Photos</button>
              </Link>
            </div>
            <div className="home-bottonbody__service_p">
              <p>
                Do you like to share your adventure? Or know which species can
                you find? Or maybe share a nice sunset? This is your place!
              </p>
            </div>
          </div>
          <div className="home-bottonbody__services__photos"></div>
          <div className="home-bottonbody__services__searchbar">
            <SearchBar />
          </div>
        </div>
        <div className="home-bottonbody__newsBox">
          <div className="home-bottonbody__newsleftbox">
            <div className="home-bottonbody__newsBoxtitle">News</div>

            <Card className="Card__NewsHome">
              <Card.Img
                variant="top"
                src={imgnewshome}
                className="Card__NewsHomeimg"
              />
              <Card.Body>
                <Card.Text>
                  <p className="Card__NewsHometext">100 Days Summer: Sunsets</p>
                  <div className="Card__NewsHomefooter">
                    <p className="Card__NewsHomefooter__category">
                      PHOTOGRAPHY
                    </p>
                    <span className="Card__NewsHomefooter__date">
                      1 Month ago
                    </span>
                  </div>
                </Card.Text>
              </Card.Body>
            </Card>
            <br />
            <Card className="Card__NewsHome">
              <Card.Img
                variant="top"
                src={img2newshome}
                className="Card__NewsHomeimg"
              />
              <Card.Body>
                <Card.Text>
                  <p className="Card__NewsHometext">
                    How to check the forecast
                  </p>
                  <div className="Card__NewsHomefooter">
                    <p className="Card__NewsHomefooter__category">SCIENCE</p>
                    <span className="Card__NewsHomefooter__date">
                      1 Month ago
                    </span>
                  </div>
                </Card.Text>
              </Card.Body>
            </Card>
            <br />
          </div>

          <div className="home-bottonbody__newsrightbox">
            <Card className="Card__NewsHome">
              <Card.Img
                variant="top"
                src={img3newshome}
                className="Card__NewsHomeimg"
              />
              <Card.Body>
                <Card.Text>
                  <p className="Card__NewsHometext">Kitesurf Wolrd Cup</p>
                  <div className="Card__NewsHomefooter">
                    <p className="Card__NewsHomefooter__category">
                      COMPETITION
                    </p>
                    <span className="Card__NewsHomefooter__date">
                      1 Month ago
                    </span>
                  </div>
                </Card.Text>
              </Card.Body>
            </Card>
            <br />
            <Card className="Card__NewsHome">
              <Card.Img
                variant="top"
                src={img4newshome}
                className="Card__NewsHomeimg"
              />
              <Card.Body>
                <Card.Text>
                  <p className="Card__NewsHometext">Photoshop your memories</p>
                  <div className="Card__NewsHomefooter">
                    <p className="Card__NewsHomefooter__category">TRAVEL</p>
                    <span className="Card__NewsHomefooter__date">
                      1 Month ago
                    </span>
                  </div>
                </Card.Text>
              </Card.Body>
            </Card>
            <br />
            <Card className="Card__NewsHome">
              <Card.Img
                variant="top"
                src={img5newshome}
                className="Card__NewsHomeimg"
              />
              <Card.Body>
                <Card.Text>
                  <p className="Card__NewsHometext">
                    Discover new places to practise surf
                  </p>
                  <div className="Card__NewsHomefooter">
                    <p className="Card__NewsHomefooter__category">TRAVEL</p>
                    <span className="Card__NewsHomefooter__date">
                      1 Month ago
                    </span>
                  </div>
                </Card.Text>
              </Card.Body>
            </Card>
            <br />
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default Home;