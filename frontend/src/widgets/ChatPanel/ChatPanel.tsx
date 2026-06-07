type Props = {
  children: React.ReactNode;
};

export default function ChatPanel({ children }: Props) {
  return (
    /* Khung ngoài cùng bọc toàn bộ màn hình chat, chuyển hẳn sang nền trắng */
    <div
      className="
        h-full
        w-full
        flex
        justify-center
        bg-white
      "
    >
      {/* Khung giới hạn nội dung bên trong */}
      <div
        className="
          max-w-[850px]
          w-full
          flex
          flex-col
          
          /* Responsive Padding: */
          /* Trên Mobile: Giảm padding xuống px-4 để tin nhắn có thêm không gian hiển thị, không bị bóp nghẹt chiều ngang */
          px-4
          
          /* Trên Máy tính (md trở lên): Tăng lên px-8 để giao diện thoáng đãng, sang trọng */
          md:px-8
        "
      >
        {children}
      </div>
    </div>
  );
}