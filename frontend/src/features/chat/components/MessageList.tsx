import MessageBubble from "./MessageBubble";
import type { Message } from "../types/message";

type Props = {
  messages?: Message[];
};

export default function MessageList({ messages = [] }: Props) {
  return (
    <div
      className="
        /* Chiếm hết không gian còn lại và tự động kích hoạt thanh cuộn dọc */
        flex-1
        overflow-y-auto
        
        /* Responsive Padding: */
        /* Trên Mobile (mặc định): Thụt lề trái/phải 4 (16px) để tin nhắn không chạm cạnh màn hình, py-4 để vừa vặn */
        px-4
        py-4
        
        /* Trên Máy tính (md trở lên): Tăng khoảng trống px-6 hoặc px-8, py-6 để giao diện thoáng đãng, sang trọng hơn */
        md:px-8
        md:py-6
        
        /* Gom các tin nhắn vào một khung flex dọc có khoảng cách ổn định */
        flex
        flex-col
        
        /* Tối ưu trải nghiệm cuộn mượt mà trên các thiết bị cảm ứng iOS/Android */
        scroll-smooth
        webkit-overflow-scrolling-touch
      "
    >
      {messages.map((message) => (
        <MessageBubble key={message.id} message={message} />
      ))}
    </div>
  );
}