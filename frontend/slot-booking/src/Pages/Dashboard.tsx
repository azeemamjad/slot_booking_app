import SlotCard from "../components/SlotCard"


function Dashboard({name = "name"}) {
    return (<>
    <div className="flex flex-wrap my-20 gap-5 align-middle justify-center">
        <SlotCard />
        <SlotCard />
        <SlotCard />
        <SlotCard />
        <SlotCard />
        <SlotCard />
        <SlotCard />
        <SlotCard />
        <SlotCard />
        <SlotCard />
        <SlotCard />
        <SlotCard />
        <SlotCard />
    </div>
    </>)
}

export default Dashboard;