import clsx from "clsx"

type Props = {
    children: React.ReactNode

    variant?:
    | "primary"
    | "ghost"

    className?: string
    onClick?: ()=>void
} 
export default function Button({
    children,
    variant="primary",
    className,
    onClick
}: Props){


    return(

<button

onClick={onClick}

className={clsx(

"rounded-xl px-4 py-2 transition",

variant==="primary" &&

"bg-white text-black",

variant==="ghost" &&

"hover:bg-zinc-800",

className

)}

>

{children}

</button>
    )

}