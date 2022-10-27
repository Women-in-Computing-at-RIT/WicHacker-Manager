import {Routes, Route, Navigate } from "react-router-dom";
import HackathonManagerLandingPage from "../pages/hmLanding";
import PageNotFound from "../pages/404Page";
import WiCHacksLanding from "../pages/wichacksLanding";
import { ProtectedComponent } from "../hocs/protectedRoute";

export default function AppRoutes(){
    return (
        <Routes>
            <Route path="/" element={<WiCHacksLanding />}/>
            <Route path="/manage" element={<ProtectedComponent component={HackathonManagerLandingPage} />} />
            <Route path="*" element={<PageNotFound />} />
        </Routes>
    )
}