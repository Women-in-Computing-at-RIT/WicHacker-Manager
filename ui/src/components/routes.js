import {Routes, Route, Navigate } from "react-router-dom";
import HackathonManagerLandingPage from "../pages/manage/hmLanding";
import PageNotFound from "../pages/404Page";
import WiCHacksLanding from "../pages/wichacksLanding";
import { ProtectedComponent } from "../hocs/protectedRoute";
import ApplicationList from "../pages/manage/applicationList";
import UserHomepage from "../pages/hackers/hackerLanding";

export default function AppRoutes(){
    return (
        <Routes>
            <Route path="/" element={<WiCHacksLanding />}/>
            <Route path="/user" element={<ProtectedComponent component={UserHomepage} />} />
            <Route path="/manage" element={<ProtectedComponent component={HackathonManagerLandingPage} />} />
            <Route path="/manage/applications" element={<ProtectedComponent component={ApplicationList} />} />
            <Route path="*" element={<PageNotFound />} />
        </Routes>
    )
}