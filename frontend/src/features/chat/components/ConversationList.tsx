import ConversationItem from "./ConversationItem";

import type { Conversation }
from "../types/conversation";

type Props = {
  conversations: Conversation[];
  activeId: string;
  onSelect: (id: string) => void;
};

export default function ConversationList({
  conversations,
  activeId,
  onSelect
}: Props) {
  return (
    <div className="flex flex-col gap-4 px-3">
      {conversations.map((conversation) => (
        <ConversationItem
          key={conversation.id}
          conversation={conversation}
          active={conversation.id === activeId}
          onSelect={onSelect}
        />
      ))}
    </div>
  );
}