import React , { useState, useContext, Fragment } from "react";
import { useForm } from "react-hook-form";
import { Link } from "react-router-dom";
import { Context } from "../store/appContext.js";
import { Redirect } from 'react-router';
import { Navbar } from "./navbar.js";
import { Footer } from "./footer.js";
import "../../styles/registerlogin.scss";


const RegisterCenter = () => {
	const { store, actions } = useContext(Context);
	const { watch, register, getValues, formState: { errors, isValid }, handleSubmit } = useForm({mode:"all"});

	const [passwordShown, setPasswordShown] = useState('');
	const [isRevealPwd, setIsRevealPwd] = useState(false);
	const hidePwdImg = "fas fa-eye-slash";
	const showPwdImg = "fas fa-eye";
	
	 
	const onSubmit = data => {
		console.log(data);
		actions.register(data);
	};

	const [formStep, setFormStep] = useState(0);

	const completeFormStep = () => {
		if (formStep === 2) return;
		setFormStep((page) => page + 1);
	  }


	return (
		<Fragment>
		<Navbar />
		<div className="register-login-form myprofile">
			<form className="register-login" onSubmit={handleSubmit(onSubmit)}>

				<div className="progressbar-regform">
        			<progress max="2" value={formStep} />
      			</div>

				<h2 className="tittle-logreg">JOIN TO WDS</h2>

				{formStep === 0 && ( 
				<section>
					<div className="form-input">
						<label htmlFor="email" className="label-relog">Email</label>
						<input
							type="text"
							name="email"
							id="email"
							placeholder="example@gmail.com"
							className="input-reglog"
							{...register("email", { required: true, pattern: /[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/ })}
						/>
						{errors.email && errors.email.type === "required" && (
							<span className="error">Email is required</span>
						)}
						{errors.email && errors.email.type === "pattern" && (
							<span className="error">Format invalid</span>
						)}
					</div>

					<div className="form-input">
						<label htmlFor="password" className="label-relog">Password</label>
						<div className="form-group"></div>
						<div className="right-inner-addon input-container">
						<input
							type={isRevealPwd ? "text" : "password"}
							name="password"
							id="password"
							placeholder="password"
							autoComplete="current-password"
							className="input-reglog"
							onChange={e => setPasswordShown(e.target.value)}
							{...register("password", { required: true, minLength: 6 })}
							
						/>
						<i
						title={isRevealPwd ? "Hide password" : "Show password"}
						className={isRevealPwd ? hidePwdImg : showPwdImg}
						onClick={() => setIsRevealPwd(prevState => !prevState)}
						/>
						</div>
						
						{errors.password && errors.password.type === "required" && (
							<span className="error">Password is required</span>
						)}
						{errors.password && errors.password.type === "minLength" && (
							<span className="error">Password is too short</span>
						)}
					</div>

					<hr />

					<div className="form-input">
						<span className="label-relog">Which waterdropper are you?</span>
						<div className="form-check form-check-reglog">
							<input className="form-check-input" type="radio" name="userType" value="waterdropper" {...register("userType")} disabled />
							<label className="form-check-label" htmlFor="waterdropper"> Athlete</label>
						</div>
						<div className="form-check form-check-reglog">
							<input className="form-check-input" type="radio" name="userType" value="center" {...register("userType")} checked />
							<label className="form-check-label" htmlFor="center"> Center or school</label>
						</div>
						{errors.userType && errors.userType.type === "required" && (
									<span className="error">Role is required</span>
								)}
					</div>



					<div className="span-logreg">
						<span>Are you an athlete? 
							<Link className="link-logreg" to="/registerWaterdropper">Sign up here</Link>
						</span>
					</div>
				</section>
				)}

				{formStep === 1 && ( 
				<section>
					<div className="form-input" className="profile-photo-label">
						<label htmlFor="photo"><i className="fas fa-upload"></i>Choose a profile photo</label>
						<input type="file"
							id="photo" name="photo"
							accept="image/png, image/jpeg" className="profile-photo"
							{...register("photo", { required: false })}
						/>
					</div>

					<div className="form-input">
						<label htmlFor="username" className="label-relog">Username</label>
						<input
							type="text"
							name="username"
							id="username"
							placeholder="username"
							className="input-reglog"
							{...register("username", { required: true })}
						/>
						{errors.username && errors.username.type === "required" && (
							<span className="error">Username is required</span>
						)}
					</div>

					<div className="form-input" >
						<span className="label-relog">Sports (check all that apply)</span>
						<div>
							<div className="form-check form-switch form-check-reglog">
							<input className="form-check-input" type="checkbox" id="scuba" name="sports" value="scuba" {...register("sports", { required: true })}/>
							<label className="form-check-label" htmlFor="scuba">Scuba diving</label>
							</div>
							<div className="form-check form-switch form-check-reglog">
							<input className="form-check-input" type="checkbox" id="surf" name="sports" value="surf" {...register("sports", { required: true })}/>
							<label className="form-check-label" htmlFor="surf">Surf</label>
							</div>
							<div className="form-check form-switch form-check-reglog">
							<input className="form-check-input" type="checkbox" id="kitesurf" name="sports" value="kitesurf" {...register("sports", { required: true })}/>
							<label className="form-check-label" htmlFor="kitesurf">Kitesurf</label>
							</div>
							<div className="form-check form-switch form-check-reglog">
							<input className="form-check-input" type="checkbox" id="snorkel" name="sports" value="snorkel" {...register("sports", { required: true })}/>
							<label className="form-check-label" htmlFor="snorkel">Snorkel</label>
							</div>
							{errors.sports && errors.sports.type === "required" && (
								<span className="error">Sport is required</span>
							)}
						</div>
					</div>

                </section>
				)} 

				{formStep === 2 && (
				<section>
					<div className="form-input">
					<label htmlFor="address" className="label-relog">Address</label>
					<input
						type="text"
						name="address"
						id="address"
						placeholder="address"
						className="input-reglog"
						{...register("address", { required: true })}
					/>
					{errors.address && errors.address.type === "required" && (
						<span className="error">Address is required</span>
					)}
				</div> 

				<div className="form-input">
					<label htmlFor="phone" className="label-relog">Phone</label>
					<input
						type="tel"
						name="phone"
						id="phone"
						placeholder="phone"
						className="input-reglog"
						{...register("phone", { required: false })}
					/>
				</div>

				<div className="form-input">
					<label htmlFor="web" className="label-relog">Web</label>
					<input
						type="text"
						name="web"
						id="web"
						placeholder="web"
						className="input-reglog"
						{...register("web", { required: false })}
					/>
				</div>
				</section>
				)}


			
				{formStep !== 2 && <button className="button-logreg" disabled={!isValid} onClick={completeFormStep}>Continue</button>}
				{formStep === 2 && (
					<button className="button-logreg" disabled={!isValid} type="submit">
					Submit
					</button>
				)}
				
			</form>
		</div>
		<Footer />
		</Fragment>
	);
};

export default RegisterCenter;