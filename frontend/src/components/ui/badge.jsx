import React from "react"
import { cn } from "./button"

function Badge({ className, variant = "default", ...props }) {
    const variants = {
        default: "border-transparent bg-brand-light text-black hover:bg-brand-default",
        secondary: "border-transparent bg-brand-blue text-white hover:bg-brand-blue/80",
        destructive: "border-transparent bg-brand-accent text-white hover:bg-brand-accent/80",
        outline: "text-foreground",
        success: "border-transparent bg-green-500 text-white"
    }

    return (
        <div
            className={cn(
                "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
                variants[variant],
                className
            )}
            {...props}
        />
    )
}

export { Badge }
