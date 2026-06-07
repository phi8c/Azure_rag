import type { Conversation } from "../types/conversation";

type Props = {
  conversation: Conversation;
  active?: boolean;
  onSelect?: (id: string) => void;
};

export default function ConversationItem({
  conversation,
  active,
  onSelect
}: Props) {
  return (
    <div
      onClick={() => onSelect?.(conversation.id)}
      className={`
        w-[92%]
        mx-auto

        flex
        items-center

        px-4
        py-4

        rounded-2xl

        cursor-pointer

        transition-all
        duration-200

        text-[14px]

        select-none

        ${
          active
            ? "bg-zinc-100 text-zinc-900 font-semibold"
            : "text-zinc-600 hover:bg-zinc-50 hover:text-zinc-900"
        }
      `}
    >
      <span className="block w-full truncate leading-6">
        {conversation.title}
      </span>
    </div>
  );
}