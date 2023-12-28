import { useEffect, useRef } from "react";

export function AlwaysScrollToBottom() {
  const elementRef = useRef();
  const prevBottom = useRef(0);
  useEffect(() => {
    const newBottom = elementRef.current.getBoundingClientRect().bottom;
    if (prevBottom.current <= window.innerHeight) {
      setTimeout(() => {
        if (elementRef.current) elementRef.current.scrollIntoView();
      }, 50);
    }
    prevBottom.current = newBottom;

    // Add scroll event listener to the parent div
    const handleScroll = () => {
      if (elementRef.current) {
        const newBottom = elementRef.current.getBoundingClientRect().bottom;
        prevBottom.current = newBottom;
      }
    };
      window.addEventListener("scroll", handleScroll);

    // Clean up the event listener when the component is unmounted
    return () => {
      if (elementRef.current) {
        window.removeEventListener(
          "scroll",
          handleScroll
        );
      }
    };
  });
  return <div ref={elementRef} />;
}
