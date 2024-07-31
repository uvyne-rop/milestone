import React, { useState } from 'react';
import {Link } from 'react-router-dom';

import {AiOutlineClose, AiOutlineMenu } from "react-icons/ai";

//state to handle navbars visibility
const Navbar = () =>{
    const [nav, setNav] = useState(false);

    //Toggle to handle the navbar's display
    const handleNav =()=> {
        setNav(!nav);
    };

    //Array containing navigation items
    const navItems = [
        {id:1, text: 'Admin', path: '/Admin'},
        {id:2, text: 'Spaces', path: '/spaces'},
        {id:3, text: 'Researches', path: '/researches'},
        {id:4, text: 'About', path: '/about'},
        {id:5, text: 'Contact', path: '/contact'},
        {id:6, text: 'Signup', path: '/Signup'},
        {id: 7, text: 'Login', path: '/Login'},
    ]
    return(
        <div className=" flex justify-between items-center h-24 max-w-[1240px] mx-auto px-4 text-white">
            {/* logo */}
            <h1 className="w-full text-3xl font-bold text-[#00df9a]">REACT.</h1>
            {/* DESKTOP NAVIGATION */}
            <ul className="hidden md:flex">
                {navItems.map(item => (
                    <li key={item.id} className="p-4 hover:bg-[#00df9a] rounded-xl m-2 cursor-pointer duration-300 hover:text-black " >
                        
                       
                        <Link to={item.path}>{item.text}</Link>
                        
                    </li>
                ))}
            </ul>
            {/*mobile navigation icon*/}
            <div onClick={handleNav} className="block md:hidden">
                 {nav ? <AiOutlineClose size={20}/> :  <AiOutlineMenu size={20}/>}
            </div>
            {/* mobile navigation menu */}
            <ul 
            className={ nav ? "fixed md:hidden left-0 top-0 w-[60%] h-full border-r border-r-gray-900 bg-[#000300] ease-in-out duration-500" : "ease-in-out w-[60%] duration-500 fixed top-0 bottom-0 left-[-100%]"

            }>
                {/* {navItems.map( item=> (
                    <li key={item.id} className=" flex p-4 hover:bg-[#00df9a] rounded-xl m-2 cursor-pointer duration-300 hover:text-black">
                        <Link to={item.id} onClick={handleNav}>
                        {item.text}
                        </Link>

                    </li> */}
                
                
                

            </ul>

        
        </div>
    )
}
export default Navbar;