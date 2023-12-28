import React, { useRef, forwardRef, useEffect } from "react";
import { Textarea } from "@chakra-ui/react";

export const GrowingTextarea = forwardRef(
  ({ lineHeight = 20, maxRows = 8, shouldFocus = true, value, ...props }, ref) => {
    const textareaRef = useRef(null);

    const handleTextareaChange = (event) => {
      adjustTextareaHeight();
    };

    const adjustTextareaHeight = () => {
      if (textareaRef.current) {
        textareaRef.current.style.height = "auto";
        textareaRef.current.style.height = `${Math.min(
          textareaRef.current.scrollHeight,
          maxRows * lineHeight
        )}px`;
      }
    };

    useEffect(() => {
      adjustTextareaHeight();
    }, [value]);

    // Also adjust on window resize
    useEffect(() => {
      window.addEventListener("resize", adjustTextareaHeight);
      return () => {
        window.removeEventListener("resize", adjustTextareaHeight);
      };
    }, []);

    const handleTextareaKeyPress = (event) => {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        event.target.form.requestSubmit();
      }
    };

    useEffect(() => {
      setTimeout(() => {
        if (textareaRef.current && shouldFocus) {
            textareaRef.current.focus();
        }
      }, 50);
    });

    const maxH = `${lineHeight * maxRows}px`;

    return (
      <Textarea
        ref={(element) => {
          textareaRef.current = element;
          if (ref) {
            if (typeof ref === "function") {
              ref(element);
            } else {
              ref.current = element;
            }
          }
        }}
        onChange={handleTextareaChange}
        onKeyPress={handleTextareaKeyPress}
        rows={1}
        value={value}
        minH="unset"
        maxH={maxH}
        overflowY="auto"
        resize="none"
        {...props}
      />
    );
  }
);
