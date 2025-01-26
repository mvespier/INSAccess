import React from 'react'
import { gsap } from 'gsap'

const { useRef, useState, useEffect, createRef } = React

/*--------------------
Items
--------------------*/
const items = [
{
  name: "Home",
  color: "#FED9EA",
  href: "/" },

{
  name: "Associative events",
  color: "#CFD6EF",
  href: "/associations" },

{
  name: "Agenda",
  color: "#9FD4F4",
  href: "/calendar" },

{
  name: "Signup",
  color: "#70D1F9",
  href: "/signup" },

{
  name: "About",
  color: "#40cefe",
  href: "/about" }
];




/*--------------------
Menu
--------------------*/

/* eslint-disable-next-line react/prop-types */
const NavBar = ({ items }) => {
  const $root = useRef();
  const $indicator1 = useRef();
  const $indicator2 = useRef();
  /* eslint-disable-next-line react/prop-types */
  const $items = useRef(items.map(createRef));
  const [active, setActive] = useState(0);

  const animate = () => {
    const menuOffset = $root.current.getBoundingClientRect();
    /* eslint-disable-next-line react/prop-types */
    const activeItem = $items.current[active].current;
    const { width, height, top, left } = activeItem.getBoundingClientRect();

    const settings = {
      x: left - menuOffset.x,
      y: top - menuOffset.y,
      width: width,
      height: height,
      /* eslint-disable-next-line react/prop-types */
      backgroundColor: items[active].color,
      ease: 'elastic.out(.7, .7)',
      duration: .8 };


    gsap.to($indicator1.current, {
      ...settings });


    gsap.to($indicator2.current, {
      ...settings,
      duration: 1 });

  };

  useEffect(() => {
    animate();
    window.addEventListener('resize', animate);

    return () => {
      window.removeEventListener('resize', animate);
    };
  }, [active]);

  return /*#__PURE__*/(
    React.createElement("div", {
      ref: $root,
      className: "menu" },

    /* eslint-disable-next-line react/prop-types */
    items.map((item, index) => /*#__PURE__*/
    React.createElement("a", {
      key: item.name,
      ref: $items.current[index],
      className: `item ${active === index ? 'active' : ''}`,
      onMouseEnter: () => {
        setActive(index);
      },
      href: item.href },

    item.name)), /*#__PURE__*/


    React.createElement("div", {
      ref: $indicator1,
      className: "indicator" }), /*#__PURE__*/

    React.createElement("div", {
      ref: $indicator2,
      className: "indicator" })));



};

export default {NavBar, items};