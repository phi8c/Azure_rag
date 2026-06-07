import Sidebar from "@/widgets/Sidebar/Sidebar";
import Header from "@/widgets/Header/Header";

type Props = {
  children: React.ReactNode;
};

export default function MainLayout({
  children
}: Props) {

  return (

    <div className="h-screen flex">

      <Sidebar />

      <div className="flex flex-col flex-1">

        <Header />

        <main className="flex-1 overflow-hidden">

          {children}

        </main>

      </div>

    </div>

  );

}