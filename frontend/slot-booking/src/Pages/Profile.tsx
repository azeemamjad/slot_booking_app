import { Canvas, useFrame } from "@react-three/fiber";
import { OrbitControls, useGLTF, Environment, Center } from "@react-three/drei";
import { useEffect, useRef, useState } from "react";
import { Github, Linkedin, Mail, MapPin, Code, Briefcase, User, Download } from "lucide-react";

import Loading from "../components/Loading";


function Model() {
    const { scene } = useGLTF("/3d_models/jin_kazama.glb");
    const modelRef = useRef<THREE.Object3D>(null!);

        // Rotate model continuously on X axis
        useFrame(() => {
            if (modelRef.current) {
                modelRef.current.rotation.y += 0.01; // speed of rotation
            }
        });
    
        return <primitive ref={modelRef} object={scene} scale={1} />;
    }

function ProfilePage() {

    const [loading, setLoading] = useState(true);
    const [activeSection, setActiveSection] = useState('about');

    useEffect(() => {
        // turn off loading after 3 seconds
        const timer = setTimeout(() => setLoading(false), 3000);
        return () => clearTimeout(timer); // cleanup
    }, []);

    if (loading)
    {
        return (
            <div>
                <Loading></Loading>
            </div>
        );
    }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white">
      {/* Header */}
      <div className="flex flex-col justify-center items-center pt-16 pb-8">
        {/* Gradient text */}
        <div className="text-6xl font-black mb-4 bg-gradient-to-r animate-bounce from-yellow-400 via-orange-400 to-yellow-600 bg-clip-text text-transparent">
          Hello, Azeem Amjad
        </div>
        <div className="text-xl text-gray-300 mb-2">Full Stack Developer & 3D Enthusiast</div>
        <div className="flex items-center text-gray-400 mb-8">
          <MapPin size={16} className="mr-2" />
          Lahore, Punjab, Pakistan
        </div>
        
        {/* Social Links */}
        <div className="flex space-x-6 mb-12">
          <a href="#" className="p-3 bg-gray-800 hover:bg-gray-700 rounded-full transition-colors duration-300 hover:scale-110 transform">
            <Github size={20} />
          </a>
          <a href="#" className="p-3 bg-gray-800 hover:bg-gray-700 rounded-full transition-colors duration-300 hover:scale-110 transform">
            <Linkedin size={20} />
          </a>
          <a href="#" className="p-3 bg-gray-800 hover:bg-gray-700 rounded-full transition-colors duration-300 hover:scale-110 transform">
            <Mail size={20} />
          </a>
        </div>

        {/* Navigation */}
        <div className="flex space-x-8 mb-8">
          {[
            { id: 'about', label: 'About', icon: User },
            { id: 'skills', label: 'Skills', icon: Code },
            { id: 'experience', label: 'Experience', icon: Briefcase }
          ].map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              onClick={() => setActiveSection(id)}
              className={`flex items-center space-x-2 px-6 py-3 rounded-full transition-all duration-300 ${
                activeSection === id
                  ? 'bg-gradient-to-r from-yellow-400 to-orange-400 text-black font-semibold'
                  : 'bg-gray-800 hover:bg-gray-700'
              }`}
            >
              <Icon size={16} />
              <span>{label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Main Content Layout */}
      <div className="flex h-[700px] w-full px-8">
        {/* Left Content Panel */}
        <div className="w-full bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-l-2xl p-8 overflow-y-auto">
          {activeSection === 'about' && (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold bg-gradient-to-r from-yellow-400 to-orange-400 bg-clip-text text-transparent">
                About Me
              </h2>
              <p className="text-gray-300 text-lg leading-relaxed">
                Passionate full-stack developer with a love for creating immersive digital experiences. 
                I specialize in modern web technologies and have a particular interest in 3D graphics 
                and interactive applications.
              </p>
              <p className="text-gray-300 text-lg leading-relaxed">
                When I'm not coding, you'll find me exploring the latest in game development, 
                experimenting with Three.js, or diving into the world of martial arts - much like 
                my favorite Tekken character, Jin Kazama.
              </p>
              <div className="mt-8">
                <button className="flex items-center space-x-2 bg-gradient-to-r from-yellow-400 to-orange-400 text-black px-6 py-3 rounded-full font-semibold hover:scale-105 transform transition-all duration-300">
                  <Download size={16} />
                  <span>Download Resume</span>
                </button>
              </div>
            </div>
          )}

          {activeSection === 'skills' && (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold bg-gradient-to-r from-yellow-400 to-orange-400 bg-clip-text text-transparent">
                Technical Skills
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-gray-900/50 p-6 rounded-xl border border-gray-600">
                  <h3 className="text-xl font-semibold mb-4 text-yellow-400">Frontend</h3>
                  <div className="flex flex-wrap gap-2">
                    {['React', 'Next.js', 'TypeScript', 'Tailwind CSS', 'Three.js', 'React Three Fiber'].map(skill => (
                      <span key={skill} className="px-3 py-1 bg-gray-700 rounded-full text-sm">{skill}</span>
                    ))}
                  </div>
                </div>
                
                <div className="bg-gray-900/50 p-6 rounded-xl border border-gray-600">
                  <h3 className="text-xl font-semibold mb-4 text-orange-400">Backend</h3>
                  <div className="flex flex-wrap gap-2">
                    {['Node.js', 'Python', 'Express', 'MongoDB', 'PostgreSQL', 'REST APIs'].map(skill => (
                      <span key={skill} className="px-3 py-1 bg-gray-700 rounded-full text-sm">{skill}</span>
                    ))}
                  </div>
                </div>
                
                <div className="bg-gray-900/50 p-6 rounded-xl border border-gray-600">
                  <h3 className="text-xl font-semibold mb-4 text-yellow-400">3D & Graphics</h3>
                  <div className="flex flex-wrap gap-2">
                    {['Blender', 'Three.js', 'WebGL', 'GLTF', 'Shader Programming'].map(skill => (
                      <span key={skill} className="px-3 py-1 bg-gray-700 rounded-full text-sm">{skill}</span>
                    ))}
                  </div>
                </div>
                
                <div className="bg-gray-900/50 p-6 rounded-xl border border-gray-600">
                  <h3 className="text-xl font-semibold mb-4 text-orange-400">Tools & DevOps</h3>
                  <div className="flex flex-wrap gap-2">
                    {['Git', 'Docker', 'AWS', 'Vercel', 'Figma', 'VS Code'].map(skill => (
                      <span key={skill} className="px-3 py-1 bg-gray-700 rounded-full text-sm">{skill}</span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeSection === 'experience' && (
            <div className="space-y-6">
              <h2 className="text-3xl font-bold bg-gradient-to-r from-yellow-400 to-orange-400 bg-clip-text text-transparent">
                Experience & Projects
              </h2>
              
              <div className="space-y-6">
                <div className="bg-gray-900/50 p-6 rounded-xl border border-gray-600 hover:border-yellow-400 transition-colors duration-300">
                  <h3 className="text-xl font-semibold text-yellow-400 mb-2">3D Portfolio Website</h3>
                  <p className="text-gray-400 mb-3">Personal Project • 2024</p>
                  <p className="text-gray-300 mb-4">
                    Interactive portfolio featuring 3D character models, custom animations, and responsive design. 
                    Built with React Three Fiber and modern web technologies.
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {['React', 'Three.js', 'Tailwind CSS', 'GLTF'].map(tech => (
                      <span key={tech} className="px-2 py-1 bg-gray-700 rounded text-sm">{tech}</span>
                    ))}
                  </div>
                </div>
                
                <div className="bg-gray-900/50 p-6 rounded-xl border border-gray-600 hover:border-orange-400 transition-colors duration-300">
                  <h3 className="text-xl font-semibold text-orange-400 mb-2">Full Stack Web Application</h3>
                  <p className="text-gray-400 mb-3">Freelance Project • 2024</p>
                  <p className="text-gray-300 mb-4">
                    Developed a complete e-commerce solution with real-time features, payment integration, 
                    and admin dashboard. Handled both frontend and backend development.
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {['Next.js', 'Node.js', 'MongoDB', 'Stripe API'].map(tech => (
                      <span key={tech} className="px-2 py-1 bg-gray-700 rounded text-sm">{tech}</span>
                    ))}
                  </div>
                </div>
                
                <div className="bg-gray-900/50 p-6 rounded-xl border border-gray-600 hover:border-yellow-400 transition-colors duration-300">
                  <h3 className="text-xl font-semibold text-yellow-400 mb-2">Interactive Game Development</h3>
                  <p className="text-gray-400 mb-3">Personal Project • 2023</p>
                  <p className="text-gray-300 mb-4">
                    Created browser-based fighting game inspired by Tekken series, featuring custom 3D models, 
                    physics simulation, and multiplayer capabilities.
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {['Three.js', 'WebGL', 'Socket.io', 'Cannon.js'].map(tech => (
                      <span key={tech} className="px-2 py-1 bg-gray-700 rounded text-sm">{tech}</span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Right Content Panel - Stats/Info */}
        <div className="w-full bg-gradient-to-br from-yellow-500/20 to-orange-500/20 backdrop-blur-sm border-t border-r border-b border-gray-700 p-8">
          <h2 className="text-2xl font-bold mb-6 text-center">Quick Stats</h2>
          
          <div className="space-y-6">
            <div className="bg-gray-900/30 p-4 rounded-xl border border-gray-600">
              <div className="text-3xl font-bold text-yellow-400 text-center">3+</div>
              <div className="text-center text-gray-300">Years Experience</div>
            </div>
            
            <div className="bg-gray-900/30 p-4 rounded-xl border border-gray-600">
              <div className="text-3xl font-bold text-orange-400 text-center">50+</div>
              <div className="text-center text-gray-300">Projects Completed</div>
            </div>
            
            <div className="bg-gray-900/30 p-4 rounded-xl border border-gray-600">
              <div className="text-3xl font-bold text-yellow-400 text-center">15+</div>
              <div className="text-center text-gray-300">Technologies Mastered</div>
            </div>
            
            <div className="bg-gray-900/30 p-4 rounded-xl border border-gray-600">
              <div className="text-3xl font-bold text-orange-400 text-center">24/7</div>
              <div className="text-center text-gray-300">Passion for Coding</div>
            </div>
          </div>
          
          <div className="mt-8 text-center">
            <h3 className="text-lg font-semibold mb-4 text-yellow-400">Current Focus</h3>
            <div className="space-y-2 text-gray-300">
              <p>🚀 WebXR Development</p>
              <p>🎮 Game Engine Integration</p>
              <p>🌟 AI-Powered Applications</p>
              <p>⚡ Performance Optimization</p>
            </div>
          </div>
        </div>

        {/* 3D Canvas */}
        <div className="w-full bg-gradient-to-br from-gray-800/50 to-gray-900/50 backdrop-blur-sm border-t border-r border-b border-gray-700 rounded-r-2xl">
            <div className="h-full relative">
              <div className="absolute top-4 left-4 z-10">
                <h3 className="text-lg font-semibold text-yellow-400 mb-2">Jin Kazama - 3D Model</h3>
                <p className="text-sm text-gray-400">Interactive 3D character showcase</p>
              </div>
              
              <Canvas
                  camera={{ position: [0, 0, 3], fov: 50 }}
                  shadows
                  gl={{ physicallyCorrectLights: true }}
                  className="rounded-r-2xl"
                  >
                  {/* Lighting */}
                  <ambientLight intensity={0.5} />
                  <directionalLight
                      position={[5, 10, 5]}
                      intensity={1.2}
                      castShadow
                      shadow-mapSize-width={1024}
                      shadow-mapSize-height={1024}
                  />
                  <hemisphereLight
                      groundColor={"#444444"}
                      intensity={0.6}
                  />

                  {/* Environment HDRI */}
                  <Environment preset="sunset" />

                  {/* Model */}
                 <Center>
                      <Model />
                  </Center>

                  {/* Camera controls */}
                  <OrbitControls enableDamping dampingFactor={0.05} />
              </Canvas>
              
              <div className="absolute bottom-4 left-4 z-10 bg-gray-900/80 backdrop-blur-sm rounded-lg p-3">
                <p className="text-sm text-gray-300">🖱️ Click and drag to rotate</p>
                <p className="text-sm text-gray-300">🔍 Scroll to zoom</p>
              </div>
            </div>
        </div>
      </div>
      
      {/* Footer */}
      <div className="w-full bg-gray-900/50 backdrop-blur-sm border-t border-gray-700 mt-8 py-8">
        <div className="text-center text-gray-400">
          <p className="mb-2">© 2024 Azeem Amjad. Crafted with passion and precision.</p>
          <p className="text-sm">Built with React, Three.js, and a lot of ☕</p>
        </div>
      </div>
    </div>
  );
}

export default ProfilePage;