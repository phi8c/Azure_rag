import {

createBrowserRouter

}
from "react-router-dom";

import ChatPage
from "@/features/chat/pages/ChatPage";
import LoginPage from "@/page/LoginPage";

export const router=

createBrowserRouter([

{

path:"/",

element:<ChatPage/>

},
{
  path: "/login",
  element: <LoginPage />
}

])