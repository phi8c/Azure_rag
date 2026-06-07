type Props = {
  icon: React.ReactNode;
  onClick?: () => void;
};
export default function IconButton({ icon, onClick }: Props) {
  return (
    <button
      onClick={onClick}
      className="
        h-10
        w-10

        rounded-full

        hover:bg-zinc-800

        flex

        items-center

        justify-center

        "
    >
      {icon}
    </button>
  );
}
